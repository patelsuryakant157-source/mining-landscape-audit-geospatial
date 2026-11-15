import ee
import geemap

# 1. Initialize GEE
ee.Initialize(project='mining-ecology-audit')

# 2. Define ROI (Dhanpuri-Amlai mining complex)
roi = ee.Geometry.BBox(81.50, 23.10, 81.65, 23.22)

# Cloud mask and scale function
def prep_landsat(img):
    # Scale optical bands to reflectance (0.0 to 1.0)
    optical = img.select('SR_B.*').multiply(0.0000275).add(-0.2)
    return img.addBands(optical, None, True)

# 3. Landsat 7 (2001 Baseline) - SWIR1, NIR, Red
l7 = (ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')
      .filterBounds(roi)
      .filterDate('2000-11-01', '2002-03-31')
      .filter(ee.Filter.lt('CLOUD_COVER', 10))
      .map(prep_landsat)
      .median()
      .clip(roi))

# 4. Landsat 8/9 (Recent) - SWIR1, NIR, Red
l8 = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
      .filterBounds(roi)
      .filterDate('2023-11-01', '2024-03-31')
      .filter(ee.Filter.lt('CLOUD_COVER', 10))
      .map(prep_landsat)
      .median()
      .clip(roi))

# False-color visualization (SWIR / NIR / Red highlights mining cuts vs vegetation)
vis_l7 = {'bands': ['SR_B5', 'SR_B4', 'SR_B3'], 'min': 0.05, 'max': 0.45}
vis_l8 = {'bands': ['SR_B6', 'SR_B5', 'SR_B4'], 'min': 0.05, 'max': 0.45}

# 5. Create Interactive Map
m = geemap.Map(center=[23.16, 81.56], zoom=13)
m.add_basemap('SATELLITE')

# Add layers
m.add_layer(l7, vis_l7, '2001 Landscape (Baseline)')
m.add_layer(l8, vis_l8, 'Recent Landscape (Active Mine & Dumps)')
m.add_layer(roi, {'color': 'red'}, 'Dhanpuri Study Extent', False)

output_file = 'dhanpuri_split_audit.html'
m.to_html(output_file)
print("Updated successfully with sharp false-color contrast!")