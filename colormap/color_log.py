import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from netCDF4 import Dataset
from matplotlib.colors import LogNorm
from matplotlib import cm
from matplotlib.animation import PillowWriter
from datetime import datetime, timedelta

def get_data(day_idx):
    # Load different dataset based on day index
    if day_idx < 300:
        dataset = Dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/tmmx_2024.nc', 'r')
    else:
        dataset = Dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/tmmx_2023.nc', 'r')
    
    var = dataset.variables['air_temperature'][:]#[day_idx, :, :]  # Only get specific day
    dataset.close()
    return var

# Load the dataset for spatial reference
dataset2 = Dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/tmmx_2023.nc', 'r')
lat = dataset2.variables['lat'][:]
lon = dataset2.variables['lon'][:]
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Define days to plot
days_to_plot = [308, 318, 333, 341, 352, 364, 7, 18, 31]

# Determine global min and max temperature values
min_temp, max_temp = np.inf, -np.inf
for day in days_to_plot:
    daily_data = get_data(day)
    min_temp = min(min_temp, np.min(daily_data))
    max_temp = max(max_temp, np.max(daily_data))

# Adjust min_temp to a small positive number if it's zero or negative
if min_temp <= 0:
    min_temp = 1e-2  # Set a small positive floor for the log scale

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

# Use LogNorm for logarithmic color scaling
norm = LogNorm(vmin=min_temp, vmax=max_temp)
cmap = cm.viridis

# Plot the first frame (for initialization)
im = ax.imshow(get_data(days_to_plot[0])[days_to_plot[0], :, :], cmap=cmap, norm=norm)

# Set up colorbar with logarithmic scale
cbar = fig.colorbar(im, ax=ax, label="Max Temperature (K)", format='%.1e')

# Title of the animation
# ax.set_title('Temperature Animation (Logarithmic Scale, Nov-Jan)', fontsize=14)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Convert day index to date string
def idxtodate(day_idx):
    if day_idx < 300:
        start_date = datetime(2024, 1, 1)
    else:
        start_date = datetime(2023, 1, 1)
        
    target_date = start_date + timedelta(days=day_idx - 1)
    return target_date.strftime("%Y-%m-%d")

# Function to update the plot for each frame
def update_frame(day_idx):
    im.set_array(get_data(day_idx)[day_idx, :, :])
    ax.set_title(f'Max Temperature(log) - {idxtodate(day_idx)}', fontsize=14)
    return [im]

# Create the animation
ani = animation.FuncAnimation(fig, update_frame, frames=days_to_plot, interval=500, blit=True)

# Save the animation as a GIF
ani.save('temperature_animation_logarithmic.gif', writer=PillowWriter(fps=1))

plt.show()
