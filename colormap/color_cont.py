import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from netCDF4 import Dataset
from matplotlib.colors import Normalize
from matplotlib import cm
from matplotlib.animation import PillowWriter
from datetime import datetime, timedelta 

def get_data(day_idx):#this only to make sure data is from correct dataset
    if day_idx < 300:
        dataset = Dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/tmmx_2024.nc', 'r')
    else:
        dataset = Dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/tmmx_2023.nc', 'r')
    
    var = dataset.variables['air_temperature'][:]#[day_idx, :, :]
    dataset.close()
    return var

# Load the dataset
dataset2 = Dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/tmmx_2023.nc', 'r')

# Extract the air_temperature variable (3D: time x lat x lon)
# air_temperature = dataset.variables['air_temperature'][:]#replaced by get_data(day_idx)
lat = dataset2.variables['lat'][:]
lon = dataset2.variables['lon'][:]
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Number of time steps (days) in the dataset
# num_days = air_temperature.shape[0]

# Select 9 evenly spaced days between November and January (uniformly spaced)
# days_to_plot = np.linspace(0, num_days - 1, 9, dtype=int)
days_to_plot = [308, 318, 333, 341, 352, 364, 7, 18, 31]

min_val, max_val = np.inf, -np.inf
for day in days_to_plot:
    daily_data = get_data(day)
    min_val = min(min_val, np.min(daily_data))
    max_val = max(max_val, np.max(daily_data))

#if log color map
# min_val = max(0,min_val)
    
# Set up the figure and axis
fig, ax = plt.subplots(figsize=(10, 8),constrained_layout = True)

# Create a colormap for the animation
cmap = cm.viridis
# norm = Normalize(vmin=np.min(get_data(days_to_plot[0])), vmax=np.max(get_data(days_to_plot[0])))
norm = Normalize(vmin=min_val, vmax=max_val)

# Plot the first frame (for initialization)
im = ax.imshow(get_data(days_to_plot[0])[days_to_plot[0], :, :], cmap=cmap, norm=norm)

# Set up colorbar
cbar = fig.colorbar(im, ax=ax, label="Max Temperature (K)")

# Title of the animation
# ax.set_title('Temperature Animation (Nov-Jan)', fontsize=14)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
# Function to update the plot for each frame

def idxtodate(day_idx):
    if day_idx < 300:
        start_date = datetime(2024, 1, 1)
    else:
        start_date = datetime(2023, 1, 1)
        
    target_date = start_date + timedelta(days=day_idx - 1)
    return target_date.strftime("%Y-%m-%d")

def update_frame(day_idx):
    # Update the image for the selected day
    im.set_array(get_data(day_idx)[day_idx, :, :])
#     ax.set_title(f'Temperature for Day {day_idx + 1} (Nov-Jan)', fontsize=14)
    ax.set_title(f'Max Temperature - {idxtodate(day_idx)}', fontsize=14)
    return [im]

# Create the animation
ani = animation.FuncAnimation(fig, update_frame, frames=days_to_plot, interval=500, blit=True)

# Save the animation as a GIF
ani.save('temperature_animation_continuous.gif', writer=PillowWriter(fps=1))

plt.show()
