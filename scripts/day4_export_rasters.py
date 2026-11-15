import ee
import geemap

# 1. Initialize Earth Engine
ee.Initialize(project='mining-ecology-audit')

# 2. Dhanpuri-Amlai Bounding Box
roi = ee.Geometry.BBox(81.50, 23.10, 81.65, 23.22)

# Cloud mask and scaling function
def prep_landsat(img):
    qa = img.select('QA_PIXEL')
    mask = qa.bitwiseAnd(1 << 4).eq(0).And(qa.bitwiseAnd(1 << 3).eq(0))
    optical = img.select('SR_B.*').multiply(0.0000275).add(-0.2)
    return img.addBands(optical, None, True).updateMask(mask)

# 3. Process 2001 Composite (Landsat 7)
l7 = (ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')
      .filterBounds(roi)
      .filterDate('2000-10-01', '2002-03-31')
      .map(prep_landsat)
      .median()
      .clip(roi))
ndvi_2001 = l7.normalizedDifference(['SR_B4', 'SR_B3']).rename('NDVI_2001')

# 4. Process 2024 Composite (Landsat 8)
l8 = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
      .filterBounds(roi)
      .filterDate('2023-10-01', '2024-03-31')
      .map(prep_landsat)
      .median()
      .clip(roi))
ndvi_2024 = l8.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI_2024')

# 5. Classify into Categorical Ecological Classes:
# Class 1 = Active Mine Pit / Overburden / Barren (NDVI < 0.22)
# Class 2 = Forest Canopy / Dense Plantation (NDVI >= 0.40)
# Class 3 = Buffer / Sparse Cover / Fallow (0.22 <= NDVI < 0.40)
def classify_landscape(ndvi_img):
    c1 = ndvi_img.lt(0.22).multiply(1)
    c2 = ndvi_img.gte(0.40).multiply(2)
    c3 = ndvi_img.gte(0.22).And(ndvi_img.lt(0.40)).multiply(3)
    return c1.add(c2).add(c3).toInt8()

classified_2001 = classify_landscape(ndvi_2001).rename('lulc_2001')
classified_2024 = classify_landscape(ndvi_2024).rename('lulc_2024')

# 6. Download GeoTIFFs to Local Disk
print("Downloading 2001 classified raster (30m resolution)...")
geemap.ee_export_image(
    classified_2001,
    filename='dhanpuri_lulc_2001.tif',
    scale=30,
    region=roi,
    file_per_band=False
)

print("Downloading 2024 classified raster (30m resolution)...")
geemap.ee_export_image(
    classified_2024,
    filename='dhanpuri_lulc_2024.tif',
    scale=30,
    region=roi,
    file_per_band=False
)

print("\nRaster exports complete! Both GeoTIFFs are saved locally.")