import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import scipy.ndimage as ndimage
import numpy as np

print("Generating Son River Buffer Encroachment Visual...")

# 1. Load calibrated rasters
with rasterio.open('dhanpuri_calibrated_2001.tif') as s1:
    g01 = s1.read(1)
with rasterio.open('dhanpuri_calibrated_2024.tif') as s2:
    g24 = s2.read(1)

# 2. Extract Son River / Water channel mask (Class 4)
river_mask = (g01 == 4) | (g24 == 4)

# 3. Compute Euclidean distance from river in pixels (30m per pixel)
distance_px = ndimage.distance_transform_edt(~river_mask)
distance_m = distance_px * 30.0

# 4. Generate discrete buffer zones
b1km = distance_m <= 1000
b2km = (distance_m > 1000) & (distance_m <= 2000)
b5km = (distance_m > 2000) & (distance_m <= 5000)

# 5. Plot setup
fig, axes = plt.subplots(1, 2, figsize=(16, 8), facecolor='white')
palette = ['#d73027', '#1a9850', '#fee08b', '#3182bd']
cmap = ListedColormap(palette)

for idx, (grid, yr) in enumerate([(g01, '2001'), (g24, '2024')]):
    ax = axes[idx]
    ax.imshow(grid, cmap=cmap, vmin=1, vmax=4, interpolation='nearest')
    
    # Overlay buffer boundary contours
    ax.contour(distance_m, levels=[1000], colors=['#e41a1c'], linewidths=1.2, linestyles='--')
    ax.contour(distance_m, levels=[2000], colors=['#ff7f00'], linewidths=1.2, linestyles='--')
    ax.contour(distance_m, levels=[5000], colors=['#377eb8'], linewidths=1.2, linestyles=':')
    
    ax.set_title(f'Son River Corridor & Mining Footprint ({yr})', fontsize=13, fontweight='bold', pad=10)
    ax.axis('off')

# Custom Legend
handles = [
    mpatches.Patch(facecolor='#d73027', label='Class 1: Active Mining / Overburden'),
    mpatches.Patch(facecolor='#3182bd', label='Class 4: Son River / Water Bodies'),
    plt.Line2D([0], [0], color='#e41a1c', linestyle='--', label='1 km Critical Riparian Buffer'),
    plt.Line2D([0], [0], color='#ff7f00', linestyle='--', label='2 km Hydrological Buffer'),
    plt.Line2D([0], [0], color='#377eb8', linestyle=':', label='5 km Macro Buffer')
]

fig.legend(handles=handles, loc='lower center', ncol=5, fontsize=9.5, bbox_to_anchor=(0.5, 0.04))
plt.subplots_adjust(bottom=0.14, wspace=0.06)

plt.savefig('son_river_buffer_audit.png', dpi=300, bbox_inches='tight')
print("Buffer map saved successfully as 'son_river_buffer_audit.png'!")
plt.show()