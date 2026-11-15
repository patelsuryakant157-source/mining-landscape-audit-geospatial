import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches

print("Rendering calibrated 4-class landscape matrices...")

# 1. Load the calibrated rasters
with rasterio.open('dhanpuri_calibrated_2001.tif') as src1:
    grid_2001 = src1.read(1)
with rasterio.open('dhanpuri_calibrated_2024.tif') as src2:
    grid_2024 = src2.read(1)

# 2. Discrete 4-class palette:
# 1 = Mining / Pit (Red), 2 = Forest (Green), 3 = Matrix/Agri (Gold), 4 = Water (Blue)
palette = ['#d73027', '#1a9850', '#fee08b', '#3182bd']
cmap = ListedColormap(palette)

# 3. Create Side-by-Side Figure
fig, axes = plt.subplots(1, 2, figsize=(16, 8), facecolor='white')

axes[0].imshow(grid_2001, cmap=cmap, vmin=1, vmax=4, interpolation='nearest')
axes[0].set_title('Dhanpuri–Amlai Complex (2001 Baseline)', fontsize=13, pad=10, fontweight='bold')
axes[0].axis('off')

axes[1].imshow(grid_2024, cmap=cmap, vmin=1, vmax=4, interpolation='nearest')
axes[1].set_title('Dhanpuri–Amlai Complex (2024 Extent)', fontsize=13, pad=10, fontweight='bold')
axes[1].axis('off')

# 4. Legend
legend_handles = [
    mpatches.Patch(facecolor='#d73027', edgecolor='black', label='Class 1: Active Pit / Overburden'),
    mpatches.Patch(facecolor='#1a9850', edgecolor='black', label='Class 2: Core Forest / Plantation'),
    mpatches.Patch(facecolor='#fee08b', edgecolor='black', label='Class 3: Matrix / Cultivated Buffer'),
    mpatches.Patch(facecolor='#3182bd', edgecolor='black', label='Class 4: Son River / Mine Sump')
]

fig.legend(
    handles=legend_handles,
    loc='lower center',
    ncol=4,
    frameon=True,
    fontsize=10,
    bbox_to_anchor=(0.5, 0.04)
)

plt.subplots_adjust(bottom=0.14, wspace=0.05)
plt.savefig('dhanpuri_calibrated_comparison.png', dpi=300, bbox_inches='tight')
print("Saved to 'dhanpuri_calibrated_comparison.png'!")
plt.show()