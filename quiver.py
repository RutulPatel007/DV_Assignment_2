#CREATING QUIVER PLOTS BASED ON LENGTH OF ARROW OR COLOUR OF ARROW AS CHANNELS FOR DENOTING WIND SPEED
#IMT2022021
#Patel Rutul Satishkumar


#Install all the necessary libraries
import numpy as np #pip install numpy
import matplotlib.pyplot as plt #pip install matplotlib
from netCDF4 import Dataset #pip install netCDF4
from mpl_toolkits.basemap import Basemap #pip install basemap
from datetime import datetime #pip install datetime
import imageio #pip install imageio
import os
from PIL import Image #pip install Image

def get_day_index_from_date(date_str):
    """Convert a date string (YYYY-MM-DD) to the day-of-year index."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    day_of_year = date_obj.timetuple().tm_yday - 1  #Subtract 1 for 0-based indexing
#     print(day_of_year)
    return day_of_year

def plot_wind_data(date_str):
    """Plot wind data for a specified date, loading the correct dataset based on the year."""
    #Determine the year and day index from the date string
    year = int(date_str[:4])
    selected_day_index = get_day_index_from_date(date_str) 

    #Select appropriate dataset paths based on the year
    #datapaths you can change accordingly(I have done this is kaggle notebooks and named the dataset dv-assignment-2)
    #You can change the below conditions according to the dataset
    if year == 2023:
        direction_file_path = '/kaggle/input/dv-assignment-2/th_2023.nc'
        speed_file_path = '/kaggle/input/dv-assignment-2/vs_2023.nc'
    elif year == 2024:
        direction_file_path = '/kaggle/input/dv-assignment-2/th_2024.nc'
        speed_file_path = '/kaggle/input/dv-assignment-2/vs_2024.nc'
    else: 
        raise ValueError("Only data for years 2023 and 2024 is available.")

    #Load datasets
    direction_data = Dataset(direction_file_path, mode='r')
    speed_data = Dataset(speed_file_path, mode='r')
    #DATA PREPROCESSING----------------------------------------------------------------------------------------------------------------------------------
    
    #Extract variables
    longitude = direction_data.variables['lon'][:]
    latitude = direction_data.variables['lat'][:]
    wind_speed_data = speed_data.variables['wind_speed'][selected_day_index][:]
    wind_direction_data = direction_data.variables['wind_from_direction'][selected_day_index][:]

    #Convert wind direction from degrees to radians
    wind_direction_rad = np.deg2rad(wind_direction_data)

    #Calculate U and V components for quiver plot
    U_component = np.sin(wind_direction_rad)
    V_component = np.cos(wind_direction_rad)

    #Normalize U and V to give arrows uniform length in one plot
    U_component = U_component / np.sqrt(U_component**2 + V_component**2)
    V_component = V_component / np.sqrt(U_component**2 + V_component**2)

    #Sample data for a more readable plot
    total_arrows = 3000
    longitude_step = len(longitude) // int(np.sqrt(total_arrows))
    latitude_step = len(latitude) // int(np.sqrt(total_arrows))

    lon_indices = np.arange(0, len(longitude), longitude_step)[:int(np.sqrt(total_arrows))]
    lat_indices = np.arange(0, len(latitude), latitude_step)[:int(np.sqrt(total_arrows))]

    #Create meshgrid of selected longitudes and latitudes
    lon_grid, lat_grid = np.meshgrid(longitude[lon_indices], latitude[lat_indices])

    #Extract U and V values at sampled points
    U_sample = U_component[lat_indices[:, None], lon_indices]
    V_sample = V_component[lat_indices[:, None], lon_indices]
    sampled_speed = wind_speed_data[lat_indices[:, None], lon_indices]
    
    
    
    #FILE SAVING SETTINGS---------------------------------------------------------------------------------------------------------------------------------------------
    
    #File path where you want to save the plots
    file_path='/kaggle/working/'
    
    #File format of image you can also change to jpg
    file_format = 'jpg'
    
    #File names you can change accordingly
    length_plot_filename = f"{file_path}length_{date_str}.{file_format}"
    color_plot_filename = f"{file_path}color_{date_str}.{file_format}"
    
    
    #PLOTTING ----------------------------------------------------------------------------------------------------------------------------------------------------------
    
    
    #Plot with colors representing wind speed
    def plot_with_color():
        plt.figure(figsize=(10, 7))

        #Set up Basemap
        m = Basemap(llcrnrlon=-123, llcrnrlat=20, urcrnrlon=-62, urcrnrlat=50,
                    projection='lcc', lat_1=33, lat_2=45, lat_0=39.5, lon_0=-98)

        #Map features
        m.drawmapboundary(fill_color='#A6CAE0') 
        m.fillcontinents(color='#ffffff', lake_color='#A6CAE0', alpha=0.7)
        m.drawcoastlines(color='#404040', linewidth=0.8)
        m.drawcountries(color='#404040', linewidth=0.6)

        m.drawparallels(np.arange(20, 51, 10), labels=[1,0,0,0], fontsize=8, color='#808080', linewidth=0.5)
        m.drawmeridians(np.arange(-120, -60, 10), labels=[0,0,0,1], fontsize=8, color='#808080', linewidth=0.5)

        #Transform lon/lat to map projection coordinates
        x, y = m(lon_grid, lat_grid)

        #Quiver plot with color-coded arrows
        quiver_plot = m.quiver(x, y, U_sample, V_sample, sampled_speed,
                               cmap=plt.cm.cividis, scale=30, width=0.0025, 
                               headwidth=1.8, headlength=3, headaxislength=4, alpha=0.9)
        plt.colorbar(quiver_plot, label='Wind Speed (m/s)', fraction=0.046, aspect=10)

        plt.title(f"Wind Direction and Speed\nContinental United States - {date_str}",
                  fontsize=14, pad=20, fontweight='bold')

        plt.tight_layout()
#         plt.show()
        plt.savefig(color_plot_filename, format=file_format, bbox_inches='tight')

        
    #Plot with arrow length representing wind speed
    def plot_with_length():
        plt.figure(figsize=(10, 7))

        #Set up Basemap
        m = Basemap(llcrnrlon=-123, llcrnrlat=20, urcrnrlon=-62, urcrnrlat=50,
                    projection='lcc', lat_1=33, lat_2=45, lat_0=39.5, lon_0=-98)

        #Map features
        m.drawmapboundary(fill_color='#A6CAE0')
        m.fillcontinents(color='#ffffff', lake_color='#A6CAE0', alpha=0.7)
        m.drawcoastlines(color='#404040', linewidth=0.8)
        m.drawcountries(color='#404040', linewidth=0.6)

        m.drawparallels(np.arange(20, 51, 10), labels=[1,0,0,0], fontsize=8, color='#808080', linewidth=0.5)
        m.drawmeridians(np.arange(-120, -60, 10), labels=[0,0,0,1], fontsize=8, color='#808080', linewidth=0.5)

        #Transform lon/lat to map projection coordinates
        x, y = m(lon_grid, lat_grid)

        #Scale U and V by wind speed
        U_scaled = U_sample * sampled_speed
        V_scaled = V_sample * sampled_speed

        quiver_plot = m.quiver(x, y, U_scaled, V_scaled, color='#4682B4',
                               scale=150, width=0.0025, headwidth=1.8, 
                               headlength=3, headaxislength=3.7, alpha=0.85)

        plt.quiverkey(quiver_plot, 0.9, 1.05, 5, '5 m/s', labelpos='E', coordinates='axes', fontproperties={'size': 10})

        plt.title(f"Wind Direction and Speed\nArrow Length Indicates Wind Speed\nContinental United States - {date_str}",
                  fontsize=14, pad=20, fontweight='bold')

        plt.tight_layout()
#         plt.show()
        plt.savefig(length_plot_filename, format=file_format, bbox_inches='tight')
        
        
  
    
    #Plots
    plot_with_length()
    
    plot_with_color()

    plt.close('all')
    
    

    

#Function only takes data as input and selects dataset according to the year 
#Date input format ---- yyyy-MM-dd
#Our dataset was November 2023, December 2023, and January 2024
#I have selected 7 days for the plots you can select according to your need
#I have plotted the wind speed and direction in interval of every 15 days of out assigned dataset
#It also saves the images in .png to your specified path which you can change in the plot_with_data function
plot_wind_data("2023-11-01") #November 1st, 2023
plot_wind_data("2023-11-15") #November 15th, 2023
plot_wind_data("2023-12-01") #December 1st, 2023
plot_wind_data("2023-12-15") #December 15th, 2023
plot_wind_data("2024-01-01") #January 1st, 2024
plot_wind_data("2024-01-15") #January 15th, 2024
plot_wind_data("2024-01-31") #January 31st, 2024


##For creating GIFs from the above generated plots

def create_gif(file_path, date_list, gif_filename, target_size=(800, 600)):
    """Create a GIF from saved images for given dates and file path, resizing to a consistent target size."""
    images = []
    for date in date_list:
        image_path = f"{file_path}{gif_filename}_{date}.jpg"
        if os.path.exists(image_path):
            # Open and resize the image to the target size
            with Image.open(image_path) as img:
                img_resized = img.resize(target_size)
                images.append(np.array(img_resized))
    
    
    #Change the path of gif according to your local setup 
    gif_path = f"{file_path}{gif_filename}.gif"
    imageio.mimsave(gif_path, images, fps=2)
    print(f"GIF saved at {gif_path}")

# List of dates for which images were saved
#You can change here according to your need
date_list = ["2023-11-01", "2023-11-15", "2023-12-01", "2023-12-15", "2024-01-01", "2024-01-15", "2024-01-31"]

# File path where the images are saved
#Change the location of the imgages created above according to your local setup
file_path = '/kaggle/working/'

#Create GIFs for color-based and length-based quiver plots

create_gif(file_path, date_list, "color")  # GIF for color-based plots
create_gif(file_path, date_list, "length")  # GIF for length-based plots


