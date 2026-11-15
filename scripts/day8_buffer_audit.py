import ee
import pandas as pd

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

# 3. Landsat Composites
l7 = (ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')
      .filterBounds(roi)
      .filterDate('2000-11-01', '2002-03-31')
      .map(prep_landsat)
      .median()
      .clip(roi))

l8 = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
      .filterBounds(roi)
      .filterDate('2023-11-01', '2024-03-31')
      .map(prep_landsat)
      .median()
      .clip(roi))

# 4. Water & Mining Masks with Calibrated Brightness
mndwi_01 = l7.normalizedDifference(['SR_B2', 'SR_B5'])
mndwi_24 = l8.normalizedDifference(['SR_B3', 'SR_B6'])

# River channel network
river_mask = mndwi_01.gt(0.0).Or(mndwi_24.gt(0.0))

# True Coal/Mining cuts (low NDVI + low Red + low SWIR)
mine_01 = (l7.normalizedDifference(['SR_B4', 'SR_B3']).lt(0.25)
           .And(l7.select('SR_B3').lt(0.15))
           .And(l7.select('SR_B5').lt(0.20))
           .And(mndwi_01.lte(0.0)))

mine_24 = (l8.normalizedDifference(['SR_B5', 'SR_B4']).lt(0.25)
           .And(l8.select('SR_B4').lt(0.15))
           .And(l8.select('SR_B6').lt(0.20))
           .And(mndwi_24.lte(0.0)))

# 5. Riparian Distance Buffers from River
print("Generating riparian distance buffers along the Son River...")
river_distance = river_mask.fastDistanceTransform(30).multiply(30).clip(roi)

buffer_zones = {
    '1 km Buffer (Critical Riparian)': river_distance.lte(1000),
    '2 km Buffer (Hydrological Zone)': river_distance.gt(1000).And(river_distance.lte(2000)),
    '5 km Buffer (Macro Catchment)': river_distance.gt(2000).And(river_distance.lte(5000))
}

# 6. Quantify Zonal Encroachment
print("Calculating mining encroachment area per buffer zone...")
records = []
pixel_area_ha = (30 * 30) / 10000.0  # 0.09 hectares per Landsat pixel

for zone_name, zone_mask in buffer_zones.items():
    # Mining in 2001
    mine_01_in_zone = mine_01.updateMask(zone_mask)
    count_01 = mine_01_in_zone.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=roi,
        scale=30,
        maxPixels=1e9
    ).getInfo()
    
    # Mining in 2024
    mine_24_in_zone = mine_24.updateMask(zone_mask)
    count_24 = mine_24_in_zone.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=roi,
        scale=30,
        maxPixels=1e9
    ).getInfo()

    val_01 = list(count_01.values())[0] or 0
    val_24 = list(count_24.values())[0] or 0

    area_01 = val_01 * pixel_area_ha
    area_24 = val_24 * pixel_area_ha
    net_change = area_24 - area_01

    records.append({
        'Buffer_Zone': zone_name,
        'Mining_Area_2001_ha': round(area_01, 2),
        'Mining_Area_2024_ha': round(area_24, 2),
        'Net_Change_ha': round(net_change, 2)
    })

buffer_df = pd.DataFrame(records)

# 7. Print Table
print("\n" + "="*85)
print("SON RIVER RIPARIAN CORRIDOR: MINING ENCROACHMENT AUDIT (2001 vs 2024)")
print("="*85)
print(buffer_df.to_string(index=False))
print("="*85)

buffer_df.to_csv('son_river_encroachment_audit.csv', index=False)
print("\nBuffer encroachment statistics saved to: son_river_encroachment_audit.csv")