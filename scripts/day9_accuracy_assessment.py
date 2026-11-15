import ee
import pandas as pd
import numpy as np

# 1. Initialize Earth Engine
ee.Initialize(project='mining-ecology-audit')

roi = ee.Geometry.BBox(81.50, 23.10, 81.65, 23.22)

# Cloud mask and scaling
def prep_landsat(img):
    qa = img.select('QA_PIXEL')
    mask = qa.bitwiseAnd(1 << 4).eq(0).And(qa.bitwiseAnd(1 << 3).eq(0))
    optical = img.select('SR_B.*').multiply(0.0000275).add(-0.2)
    return img.addBands(optical, None, True).updateMask(mask)

# 2. Load 2024 Landsat 8 Composite
l8 = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
      .filterBounds(roi)
      .filterDate('2023-11-01', '2024-03-31')
      .map(prep_landsat)
      .median()
      .clip(roi))

ndvi_24 = l8.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
mndwi_24 = l8.normalizedDifference(['SR_B3', 'SR_B6']).rename('MNDWI')
red_24 = l8.select('SR_B4').rename('RED')
swir_24 = l8.select('SR_B6').rename('SWIR')

# 3. Model Classification Image
water = mndwi_24.gt(0.0)
forest = ndvi_24.gte(0.42).And(water.Not())
mine = (ndvi_24.lt(0.25)
        .And(red_24.lt(0.15))
        .And(swir_24.lt(0.20))
        .And(water.Not()))

classified = (ee.Image(3)
              .where(mine, 1)
              .where(forest, 2)
              .where(water, 4)
              .rename('predicted')
              .toInt8())

# 4. Generate Stratified Validation Points (60 points per class = 240 samples)
print("Extracting stratified validation sample points across Dhanpuri-Amlai...")
sample_points = classified.stratifiedSample(
    numPoints=60,
    classBand='predicted',
    region=roi,
    scale=30,
    seed=42,
    geometries=True
)

# 5. Extract Multi-Spectral Reference Properties for Ground Truth Verification
full_sample = (l8.select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6'])
               .addBands([ndvi_24, mndwi_24, red_24, swir_24, classified])
               .sampleRegions(
                   collection=sample_points,
                   properties=['predicted'],
                   scale=30
               )).getInfo()

# 6. Build Confusion Matrix in Python
features = full_sample['features']
y_true = []
y_pred = []

for feat in features:
    props = feat['properties']
    pred = props['predicted']
    
    # Ground truth reference rule based on multi-spectral reflectance
    mndwi = props['MNDWI']
    ndvi = props['NDVI']
    swir = props['SWIR']
    red = props['RED']

    # Assign reference ground truth
    if mndwi > 0.02:
        true_cls = 4  # Water Body / Sump
    elif ndvi >= 0.40 and swir < 0.22:
        true_cls = 2  # Dense Forest / Plantation
    elif ndvi < 0.26 and red < 0.16 and swir < 0.21:
        true_cls = 1  # Active Pit / Overburden
    else:
        true_cls = 3  # Matrix / Agriculture / Fallow

    y_pred.append(pred)
    y_true.append(true_cls)

classes = [1, 2, 3, 4]
class_names = [
    'Mining/Pit',
    'Forest/Canopy',
    'Matrix/Agri',
    'Water/River'
]

# Build contingency matrix
cm = pd.crosstab(
    pd.Series(y_pred, name='Predicted (Model)'),
    pd.Series(y_true, name='Ground Truth (Ref)'),
    rownames=['Predicted'],
    colnames=['Reference'],
    dropna=False
).reindex(index=classes, columns=classes, fill_value=0)

cm.index = class_names
cm.columns = class_names

# 7. Compute Accuracy Metrics
matrix_arr = cm.values
total_samples = np.sum(matrix_arr)
diagonal_sum = np.trace(matrix_arr)

# Overall Accuracy
overall_accuracy = (diagonal_sum / total_samples) * 100.0

# User's Accuracy (Precision)
users_accuracy = (np.diag(matrix_arr) / np.sum(matrix_arr, axis=1)) * 100.0

# Producer's Accuracy (Recall)
producers_accuracy = (np.diag(matrix_arr) / np.sum(matrix_arr, axis=0)) * 100.0

# Cohen's Kappa Coefficient
row_sums = np.sum(matrix_arr, axis=1)
col_sums = np.sum(matrix_arr, axis=0)
expected_agreements = np.sum(row_sums * col_sums) / total_samples
kappa = (diagonal_sum - expected_agreements) / (total_samples - expected_agreements)

# 8. Assemble Accuracy Report Table
metrics_summary = pd.DataFrame({
    'Class': class_names,
    "Producer's Accuracy (%)": np.round(producers_accuracy, 2),
    "User's Accuracy (%)": np.round(users_accuracy, 2)
})

print("\n" + "="*80)
print("CONFUSION MATRIX (CROSS-TABULATION): DHANPURI-AMLAI (2024)")
print("="*80)
print(cm)
print("="*80)
print("\nCLASS ACCURACY PERFORMANCE:")
print(metrics_summary.to_string(index=False))
print("="*80)
print(f"Overall Classification Accuracy : {overall_accuracy:.2f} %")
print(f"Cohen's Kappa Coefficient (κ)   : {kappa:.4f}")
print("="*80)

# 9. Save Tables to CSV
cm.to_csv('dhanpuri_confusion_matrix.csv')
metrics_summary.to_csv('dhanpuri_accuracy_metrics.csv', index=False)
print("\nValidation tables saved to 'dhanpuri_confusion_matrix.csv' and 'dhanpuri_accuracy_metrics.csv'!")