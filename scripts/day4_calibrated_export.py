import ee
import geemap

# 1. Initialize Earth Engine
ee.Initialize(project='mining-ecology-audit')

# 2. Study Area Bounding Box (Dhanpuri-Amlai Basin)
roi = ee.Geometry.BBox(81.50, 23.10, 81.65, 23.22)

# Cloud mask and scaling
def prep_landsat(img):
    qa = img.select('QA_PIXEL')
    mask = qa.bitwiseAnd(1 << 4).eq(0).And(qa.bitwiseAnd(1 << 3).eq(0))
    optical = img.select('SR_B.*').multiply(0.0000275).add(-0.2)
    return img.addBands(optical, None, True).updateMask(mask)

# 3. Landsat 7 (2001 Baseline)
l7 = (ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')
      .filterBounds(roi)
      .filterDate('2000-11-01', '2002-03-31')
      .map(prep_landsat)
      .median()
      .clip(roi))

ndvi_01 = l7.normalizedDifference(['SR_B4', 'SR_B3']).rename('NDVI')
mndwi_01 = l7.normalizedDifference(['SR_B2', 'SR_B5']).rename('MNDWI')
red_01 = l7.select('SR_B3')
swir_01 = l7.select('SR_B5')

# 4. Landsat 8 (2024 Extent)
l8 = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
      .filterBounds(roi)
      .filterDate('2023-11-01', '2024-03-31')
      .map(prep_landsat)
      .median()
      .clip(roi))

ndvi_24 = l8.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
mndwi_24 = l8.normalizedDifference(['SR_B3', 'SR_B6']).rename('MNDWI')
red_24 = l8.select('SR_B4')
swir_24 = l8.select('SR_B6')

# 5. Calibrated Classifier with Brightness Thresholding
def classify_landscape(ndvi, mndwi, red, swir, forest_thresh):
    # Water: Son River, reservoirs, and mine pit sumps
    water = mndwi.gt(0.0).rename('water')
    
    # Forest Canopy: High persistent vegetation index
    forest = ndvi.gte(forest_thresh).And(water.Not()).rename('forest')
    
    # Genuine Coal Pit / Active Overburden:
    # Low NDVI AND low reflectance in Red/SWIR (dark absorption characteristic of coal)
    # Dry farm soil/sand reflects brightly (> 0.16) and gets rejected into Class 3
    mine = (ndvi.lt(0.25)
            .And(red.lt(0.15))
            .And(swir.lt(0.20))
            .And(water.Not())).rename('mine')
    
    # Class mapping: 1=Mine, 2=Forest, 3=Matrix/Agri/Fallow, 4=Water
    cls = (ee.Image(3)
           .where(mine, 1)
           .where(forest, 2)
           .where(water, 4)
           .toInt8())
    return cls

classified_2001 = classify_landscape(ndvi_01, mndwi_01, red_01, swir_01, forest_thresh=0.38)
classified_2024 = classify_landscape(ndvi_24, mndwi_24, red_24, swir_24, forest_thresh=0.42)

# 6. Export Refined Rasters
print("Downloading spectral-brightness calibrated 2001 raster...")
geemap.ee_export_image(
    classified_2001,
    filename='dhanpuri_calibrated_2001.tif',
    scale=30,
    region=roi,
    file_per_band=False
)

print("Downloading spectral-brightness calibrated 2024 raster...")
geemap.ee_export_image(
    classified_2024,
    filename='dhanpuri_calibrated_2024.tif',
    scale=30,
    region=roi,
    file_per_band=False
)

print("\nRefined GeoTIFFs downloaded successfully!")