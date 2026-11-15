import ee
import geemap

# 1. Initialize Earth Engine
ee.Initialize(project='mining-ecology-audit')

# 2. Define Dhanpuri-Amlai Bounding Box
roi = ee.Geometry.BBox(81.50, 23.10, 81.65, 23.22)

# 3. Bitmask Cloud and Shadow Masking for Landsat Collection 2
def mask_landsat_sr(image):
    # Bit 3 = Cloud, Bit 4 = Cloud Shadow
    qa = image.select('QA_PIXEL')
    cloud_shadow_mask = qa.bitwiseAnd(1 << 4).eq(0)
    cloud_mask = qa.bitwiseAnd(1 << 3).eq(0)
    mask = cloud_shadow_mask.And(cloud_mask)
    
    # Scale optical bands (0.0000275 scale factor, -0.2 offset)
    optical = image.select('SR_B.*').multiply(0.0000275).add(-0.2)
    return image.addBands(optical, None, True).updateMask(mask)

# 4. Helper function to compute and append NDVI
def add_ndvi_l7(image):
    ndvi = image.normalizedDifference(['SR_B4', 'SR_B3']).rename('NDVI')
    return image.addBands(ndvi)

def add_ndvi_l8(image):
    ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
    return image.addBands(ndvi)

# 5. Build Post-Monsoon Composites (October to March)
print("Querying and filtering satellite collections...")

# Baseline 2000-2002 (Landsat 7)
l7_col = (ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')
          .filterBounds(roi)
          .filterDate('2000-10-01', '2002-03-31')
          .map(mask_landsat_sr)
          .map(add_ndvi_l7))
comp_2001 = l7_col.median().clip(roi)
ndvi_2001 = comp_2001.select('NDVI')

# Recent 2023-2024 (Landsat 8)
l8_col = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
          .filterBounds(roi)
          .filterDate('2023-10-01', '2024-03-31')
          .map(mask_landsat_sr)
          .map(add_ndvi_l8))
comp_2024 = l8_col.median().clip(roi)
ndvi_2024 = comp_2024.select('NDVI')

# 6. Compute Delta NDVI (2024 minus 2001)
delta_ndvi = ndvi_2024.subtract(ndvi_2001).rename('Delta_NDVI')

# 7. Spatial Summary Statistics
stats_delta = delta_ndvi.reduceRegion(
    reducer=ee.Reducer.mean().combine(
        reducer2=ee.Reducer.minMax(), sharedInputs=True
    ),
    geometry=roi,
    scale=30,
    maxPixels=1e9
).getInfo()

print("--- Dhanpuri Ecological Baseline Statistics ---")
for k, v in stats_delta.items():
    print(f"{k}: {v:.4f}")

# 8. Render to Interactive HTML Map
m = geemap.Map(center=[23.16, 81.56], zoom=13)
m.add_basemap('HYBRID')

# Palette styles
ndvi_palette = ['#8c510a', '#d8b365', '#f6e8c3', '#c7eae5', '#5ab4ac', '#01665e']
delta_palette = ['#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641']

m.add_layer(ndvi_2001, {'min': 0.0, 'max': 0.7, 'palette': ndvi_palette}, 'NDVI 2001 (Baseline)')
m.add_layer(ndvi_2024, {'min': 0.0, 'max': 0.7, 'palette': ndvi_palette}, 'NDVI 2024 (Current)')
m.add_layer(delta_ndvi, {'min': -0.4, 'max': 0.4, 'palette': delta_palette}, 'Delta NDVI (2001 to 2024)')
m.add_layer(roi, {'color': 'red'}, 'ROI Boundary', False)

output_html = 'dhanpuri_ndvi_trajectory.html'
m.to_html(output_html)
print(f"\nMap output written to: {output_html}")