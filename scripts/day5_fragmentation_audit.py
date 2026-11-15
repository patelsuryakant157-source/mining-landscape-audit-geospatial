import pylandstats as pls
import pandas as pd

print("Running Calibrated PyLandStats Audit for Dhanpuri-Amlai...")

# Load calibrated GeoTIFFs
ls_2001 = pls.Landscape('dhanpuri_calibrated_2001.tif', res=(30, 30))
ls_2024 = pls.Landscape('dhanpuri_calibrated_2024.tif', res=(30, 30))

metrics = ['total_area', 'proportion_of_landscape', 'number_of_patches', 'area_mn', 'edge_density']

df_2001 = ls_2001.compute_class_metrics_df(metrics=metrics)
df_2024 = ls_2024.compute_class_metrics_df(metrics=metrics)

class_names = {
    1: 'Active Pit / Overburden Dump',
    2: 'Core Forest Canopy / Sal Tracts',
    3: 'Matrix / Cultivated / Buffer',
    4: 'Son River / Mine Sump / Water'
}

df_2001['class_name'] = df_2001.index.map(class_names)
df_2024['class_name'] = df_2001.index.map(class_names)

df_2001['Year'] = 2001
df_2024['Year'] = 2024

comparison_df = pd.concat([
    df_2001.reset_index(),
    df_2024.reset_index()
]).sort_values(by=['class_val', 'Year'])

comparison_df.rename(columns={
    'class_val': 'Class_ID',
    'total_area': 'Area_ha',
    'proportion_of_landscape': 'Landscape_Pct',
    'number_of_patches': 'Patch_Count',
    'area_mn': 'Mean_Patch_Size_ha',
    'edge_density': 'Edge_Density_m_per_ha'
}, inplace=True)

print("\n" + "="*95)
print("DHANPURI-AMLAI CALIBRATED LANDSCAPE AUDIT (2001 vs 2024)")
print("="*95)
cols = ['Year', 'class_name', 'Area_ha', 'Landscape_Pct', 'Patch_Count', 'Mean_Patch_Size_ha', 'Edge_Density_m_per_ha']
print(comparison_df[cols].to_string(index=False))
print("="*95)

comparison_df.to_csv('dhanpuri_fragmentation_audit.csv', index=False)
print("\nUpdated calibrated statistics saved to: dhanpuri_fragmentation_audit.csv")