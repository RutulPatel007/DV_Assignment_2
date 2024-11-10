#CREATING STREAMLINES AND GIF USING STREAMLINE PLOTS
#IMT2022021
#Patel Rutul Satishkumar
#You can change the dataset paths and output file paths according to your setup 


import os
import numpy as np
import xarray as xr
import imageio.v2 as imageio
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import RegularGridInterpolator
from matplotlib.colors import LinearSegmentedColormap, Normalize

# Load datasets for wind direction and speed
dir_data2 = xr.open_dataset('/kaggle/input/dv-assignment-2/th_2023.nc')
speed_data2 = xr.open_dataset('/kaggle/input/dv-assignment-2/vs_2023.nc')
dir_data1 = xr.open_dataset('/kaggle/input/dv-assignment-2/th_2024.nc')
speed_data1 = xr.open_dataset('/kaggle/input/dv-assignment-2/vs_2024.nc')
downsample_factor = 10

#List of days to visualize (selected days covering specific storms)
#Covering 3 months of time span by taking interval of 10 days(November 2023 to January 2024)
day_list = [304,314,324,334,344,354,364,9,19,29]
num_frames = len(day_list)

# Normalize wind speed values to a range for color mapping in plots
norm = Normalize(vmin=0, vmax=10)

# Main function to generate streamlines images for each selected day
def streamline_images():

    for day in day_list:
        # Initialize plot for each day
        #2023 if November and December
        if day > 300:
            dir_data = dir_data2
            speed_data = speed_data2
        else:#January 2024
            dir_data = dir_data1
            speed_data = speed_data1
            
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create a Basemap projection for the region (USA and surroundings)
        m = Basemap(llcrnrlon=-123, llcrnrlat=20, urcrnrlon=-62, urcrnrlat=50,
                   projection='lcc', lat_1=33, lat_2=45, lat_0=39.5, lon_0=-98, ax=ax)

        # Define grid resolution based on map boundaries (50km spacing)
        nx = int((m.xmax - m.xmin) / 50000)
        ny = int((m.ymax - m.ymin) / 50000)

        # Generate mesh grid for x and y coordinates in the map's projection
        x = np.linspace(m.xmin, m.xmax, nx)
        y = np.linspace(m.ymin, m.ymax, ny)
        x_grid, y_grid = np.meshgrid(x, y)

        # Convert projection grid to geographic coordinates (lat/lon)
        lon_grid, lat_grid = m(x_grid, y_grid, inverse=True)

        # Extract wind direction and speed for the specific day from datasets
        wind_dir = dir_data['wind_from_direction'].isel(day=day)
        wind_speed = speed_data['wind_speed'].isel(day=day)

        # Convert wind direction to radians and calculate U, V components
        wind_rad = np.deg2rad(270 - wind_dir)  # Convert from meteorological to math convention
        U = wind_speed * np.cos(wind_rad)      # U component of wind (east-west)
        V = wind_speed * np.sin(wind_rad)      # V component of wind (north-south)

        # Get latitude and longitude arrays from dataset for interpolation
        lats = dir_data.lat.values
        lons = dir_data.lon.values

        # Set up interpolators to resample wind data on the map grid
        U_interp = RegularGridInterpolator((lats, lons), U.values,
                                           bounds_error=False, fill_value=0)
        V_interp = RegularGridInterpolator((lats, lons), V.values,
                                           bounds_error=False, fill_value=0)
        speed_interp = RegularGridInterpolator((lats, lons), wind_speed.values,
                                               bounds_error=False, fill_value=0)

        # Interpolate U, V, and speed on the projection grid
        points = np.column_stack((lat_grid.flatten(), lon_grid.flatten()))
        U_grid = U_interp(points).reshape(x_grid.shape)
        V_grid = V_interp(points).reshape(x_grid.shape)
        speed_grid = speed_interp(points).reshape(x_grid.shape)

        # Rotate U and V to align with the map's grid orientation
        U_grid, V_grid = m.rotate_vector(U_grid, V_grid, lon_grid, lat_grid)

        # Draw base map details (boundaries, continents, coastlines)
        m.drawmapboundary(fill_color='#A6CAE0')
        m.fillcontinents(color='#ffffff', lake_color='#A6CAE0', alpha=0.7)
        m.drawcoastlines(color='#404040', linewidth=0.8)
        m.drawcountries(color='#404040', linewidth=0.6)
        m.drawparallels(np.arange(20,51,10), labels=[1,0,0,0], fontsize=8, color='#808080', linewidth=0.5)
        m.drawmeridians(np.arange(-120,-60,10), labels=[0,0,0,1], fontsize=8, color='#808080', linewidth=0.5)
    
        # Plot wind streamlines, colored by wind speed, with density set for clarity
        stream = ax.streamplot(x, y, U_grid, V_grid,
                               color=speed_grid,
                               cmap=plt.cm.bone_r,
                               norm=norm,
                               linewidth=1,
                               density=2)

        # Add color bar to indicate wind speed scale
        plt.colorbar(stream.lines, label='Wind Speed (m/s)', orientation='vertical', fraction=0.046, aspect=10)

        # Set title for each frame and adjust layout for clear output
        plt.title(f"Wind Streamlines - Day {day}", fontsize=14, pad=20)
        plt.tight_layout()

        # Save each frame as an individual image in the specified directory
#         plt.show()
        fig.savefig(f'/kaggle/working/day_{day:02d}.png', format='png')
        plt.close(fig)  # Close the figure to free memory

# Function to compile saved images into a GIF animation
def gif_creator():
    images = [] #Image list to create GIF
    for day in day_list:
        # Read each saved image and add it to the list for GIF creation
        images.append(imageio.imread(f'/kaggle/working/day_{day:02d}.png'))
    # Save all frames into a single GIF file with a specified frame rate
    imageio.mimsave(f'/kaggle/working/streamlines_{num_frames}.gif', images, fps=2)

# Generate the images and create the GIF
streamline_images()
gif_creator()