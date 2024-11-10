# -*- coding: utf-8 -*-
"""contour.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LeyhAmQ6WQc_fW4WBer0DnN0hYemXN26
"""

!pip install netCDF4
!pip install xarray
!pip install matplotlib
!pip install numpy

import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

path_sph = '/kaggle/input/gridmet-dataset/netCDF4_datasets/sph_2023.nc'
data_sph = nc.Dataset(path_sph,'r')
print(data_sph)
print(data_sph.variables.keys())

path_pr = 'pr_2024.nc'
data_pr = nc.Dataset(path_pr,'r')
print(data_pr)
print(data_pr.variables.keys())

path_sph = '/kaggle/input/gridmet-dataset/netCDF4_datasets/srad_2024.nc'
data_sph = nc.Dataset(path_sph,'r')
print(data_sph)
print(data_sph.variables.keys())

path_tmmn = 'tmmn_2023.nc'
data_tmmn = nc.Dataset(path_tmmn,'r')
print(data_tmmn)
print(data_tmmn.variables.keys())

path_rmin = 'rmin_2024.nc'
data_rmin = nc.Dataset(path_rmin,'r')
print(data_rmin)
print(data_rmin.variables.keys())

path_vs = 'th_2024.nc'
data_vs = nc.Dataset(path_vs,'r')
print(data_vs)
print(data_vs.variables.keys())

path_th = 'th_2024.nc'
data_th = nc.Dataset(path_th,'r')
print(data_th)
print(data_th.variables.keys())

path_bi = 'bi_2024.nc'
data_bi = nc.Dataset(path_bi,'r')
print(data_bi)
print(data_bi.variables.keys())

path_fm = 'fm100_2024.nc'
data_fm = nc.Dataset(path_fm,'r')
print(data_fm)
print(data_fm.variables.keys())

path_etr = 'etr_2024.nc'
data_etr = nc.Dataset(path_etr,'r')
print(data_etr)
print(data_etr.variables.keys())

"""we can try a combination of **high temp and low humidity** to showcase:

**Inference**: This combination can help identify regions with high heat and low humidity, which are typically more prone to drought and wildfire risks. It can also provide insights into potential heat stress on crops and livestock.

let us do 4 concluding visualizations:

# **Heat Stress**:
**Variables**:
Maximum temperature, minimum relative humidity, and wind velocity.


**Inference**: This combination is also effective for identifying areas at risk of heat stress, especially in urban areas where heat can be exacerbated by low humidity and strong, drying winds.
*   **High Temperature and Low Humidity:** These conditions can make temperatures feel hotter than they are, increasing risks of dehydration and heat-related illnesses.
*   **Wind Velocity & Direction:** While wind can sometimes offer relief, strong, hot, dry winds (like Santa Ana winds in California) can amplify heat stress.
"""

import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from datetime import datetime, timedelta

# Load datasets
ds_tmmx1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/tmmx_2023.nc')  # Max temperature dataset
ds_tmmx2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/tmmx_2024.nc')  # Max temperature dataset
ds_hm1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/rmin_2023.nc')    # Min relative humidity dataset
ds_hm2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/rmin_2024.nc')    # Min relative humidity dataset
ds_wind1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/vs_2023.nc')  # Wind velocity dataset
ds_wind2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/vs_2024.nc')  # Wind velocity dataset
ds_th1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/th_2023.nc')  # Wind direction dataset (assumes u and v components)
ds_th2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/th_2024.nc')  # Wind direction dataset (assumes u and v components)

# Select the 9 days for the animation (adjust indices as needed)
# days_indices = np.linspace(0, len(ds_tmmx['day']) - 1, 9, dtype=np.float64).astype(int)
day_indices = [310,321,336,341,352,364,7,18,31]
# Sampling factor to reduce grid size for visualization
sample_factor = 18

# Sample latitude and longitude grids
lat = ds_tmmx2['lat'][::sample_factor]
lon = ds_tmmx2['lon'][::sample_factor]

# Create figure and initial plot
# Initialize wind plot (quiver) variables
fig, axes = plt.subplots(1,2,figsize=(16, 6),constrained_layout = True)
ax_contour, ax_quiver = axes
temp_cbar = hum_cbar = quiver_cbar = None

norm = Normalize(vmin=0, vmax=10)

def idxtodate(day_idx):
    if(day_idx<300):
        start_date = datetime(2024, 1, 1)
    else:
        start_date = datetime(2023, 1, 1)

    target_date = start_date + timedelta(days=day_idx - 1)
    return target_date.strftime("%Y-%m-%d")

def update(day_idx):
    global temp_cbar, hum_cbar, quiver_cbar

    ax_contour.cla()
    ax_quiver.cla()

    # Get temperature, humidity, and wind data for the specific day
    if(day_idx<300):
        max_temp = ds_tmmx2['air_temperature'][day_idx, :, :]
        rel_hum = ds_hm2['relative_humidity'][day_idx, :, :]
        u_wind = ds_wind2['wind_speed'][day_idx, :, :]  # Assuming wind dataset has 'u_component'
        v_dir = ds_th2['wind_from_direction'][day_idx, :, :]  # and 'v_component' for wind velocity

    else:
        max_temp = ds_tmmx1['air_temperature'][day_idx, :, :]
        rel_hum = ds_hm1['relative_humidity'][day_idx, :, :]
        u_wind = ds_wind1['wind_speed'][day_idx, :, :]  # Assuming wind dataset has 'u_component'
        v_dir = ds_th1['wind_from_direction'][day_idx, :, :]  # and 'v_component' for wind velocity


    # Sample data for visualization
    max_temp_sample = max_temp[::sample_factor, ::sample_factor]
    rel_hum_sample = rel_hum[::sample_factor, ::sample_factor]
    speed_sample = u_wind[::sample_factor, ::sample_factor]
    v_dir_sample = v_dir[::sample_factor, ::sample_factor]

    #calculate u nad v components for the quiver plot
    U = speed_sample * np.cos(np.radians(270 - v_dir_sample))
    V = speed_sample * np.sin(np.radians(270 - v_dir_sample))

    magnitude = np.sqrt(U**2 + V**2)
    u_wind_norm = U / magnitude
    v_wind_norm = V / magnitude

    # Plot filled contours for relative humidity
    contour = ax_contour.contourf(lon, lat, rel_hum_sample, levels=20, cmap="YlGnBu", alpha=0.7, extend="both")

    # Plot contour lines for temperature
    temp_contour = ax_contour.contour(lon, lat, max_temp_sample, cmap='Reds', levels=10, linewidths=1.5)
    # plt.clabel(temp_contour, inline=True, fontsize=10, fmt='%1.0f°C')

    # Add wind velocity as arrows (quiver plot)
#     quiver = ax.quiver(lon, lat, u_wind_norm, v_wind_norm,speed_sample, cmap='viridis', scale=100, color='purple', alpha=0.7)
    # quiver = ax.quiver(lon, lat, u_wind_norm, v_wind_norm,speed_sample, cmap='viridis', scale=100, alpha=0.7)
    quiver = ax_quiver.quiver(
        lon_grid, lat_grid, U, V, speed_sample,
        cmap='viridis', scale=200, norm=norm, alpha=1
    )
    # Add color bar for humidity (only create it once)
    if hum_cbar is None:
        hum_cbar = fig.colorbar(contour, ax=ax_contour, label="Relative Humidity (%)")

    if temp_cbar is None:
        temp_cbar = fig.colorbar(temp_contour, ax=ax_contour, label="Max Temperature (K)")

    if quiver_cbar is None:
        quiver_cbar = fig.colorbar(quiver, ax=ax_quiver, label="Wind Speed (m/s)")

    # Update title to reflect current day index
    # ax.set_title(f"Temperature, Humidity, and Wind on Day {day_idx}")
    ax_contour.set_title("Heat Stress Analysis - "+  idxtodate(day_idx) + "\nContour Lines: Max Temperature (°C)")
    ax_contour.set_xlabel("Longitude")
    ax_contour.set_ylabel("Latitude")

    ax_quiver.set_title("Wind Speed & Direction - "+ idxtodate(day_idx))
    ax_quiver.set_xlabel("Longitude")
    ax_quiver.set_ylabel("Latitude")

# Set up FuncAnimation
ani = FuncAnimation(fig, update, frames=day_indices, repeat=True)

# Save the animation as a GIF
ani.save("heat_stress.gif", writer='pillow', fps=1)

plt.close(fig)  # Close the figure when done

"""# **Fire Danger Analysis**
**Variables:**  Maximum Temperature, Dead Fuel Moisture (100-hour and 1000-hour), and Burning Index.

**Inference**:  High temperatures and low dead fuel moisture levels indicate conditions conducive to wildfires, especially in dry forests. The Burning Index helps quantify fire intensity.

**Visualization**:
*   Contour Lines: Maximum Temperature.
*   Filled Contours: Dead Fuel Moisture (100-hour or 1000-hour).
*   Overlay: Burning Index as color-coded markers or shaded regions.

the below code is to have the scatter plot beside the contour plot and not overlapping it:
"""

import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from datetime import datetime, timedelta

# Load datasets
ds_tmmx1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/tmmx_2023.nc')          # Max temperature dataset
ds_tmmx2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/tmmx_2024.nc')          # Max temperature dataset
ds_dfm1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/fm100_2023.nc')          # Dead fuel moisture dataset (100-hour or 1000-hour)
ds_dfm2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/fm100_2024.nc')          # Dead fuel moisture dataset (100-hour or 1000-hour)
ds_bi1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/bi_2023.nc')              # Burning index dataset
ds_bi2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/bi_2024.nc')              # Burning index dataset

# Select the days for the animation (adjust indices as needed)
days_indices = [310, 321, 336, 341, 352, 364, 7, 18, 31]
sample_factor = 18  # Sampling factor to reduce grid size for visualization

# Sample latitude and longitude grids and adjust for sample factor
lat = ds_tmmx2['lat'][::sample_factor]
lon = ds_tmmx2['lon'][::sample_factor]
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Create figure with two subplots side-by-side
fig,axes = plt.subplots(1, 2, figsize=(16, 6), constrained_layout = True)
ax_contour, ax_scatter = axes
dfm_cbar = temp_cbar = bi_cbar = None


def idxtodate(day_idx):
    """Convert day index to date for labeling purposes."""
    if day_idx < 300:
        start_date = datetime(2024, 1, 1)
    else:
        start_date = datetime(2023, 1, 1)
    target_date = start_date + timedelta(days=day_idx - 1)
    return target_date.strftime("%Y-%m-%d")

def update(day_idx):
    global bi_cbar, dfm_cbar, temp_cbar

    ax_scatter.cla()
    ax_contour.cla()

#     # Clear previous plots
#     if contour:
#         for c in contour.collections:
#             c.remove()
#     if temp_contour:
#         for c in temp_contour.collections:
#             c.remove()
#     if scatter:
#         scatter.remove()

    # Get temperature, dead fuel moisture, and burning index data for the specific day
    if day_idx < 300:
        max_temp = ds_tmmx2['air_temperature'][day_idx, :, :]
        dead_fuel_moisture = ds_dfm2['dead_fuel_moisture_100hr'][day_idx, :, :]
        burn_index = ds_bi2['burning_index_g'][day_idx, :, :]
    else:
        max_temp = ds_tmmx1['air_temperature'][day_idx, :, :]
        dead_fuel_moisture = ds_dfm1['dead_fuel_moisture_100hr'][day_idx, :, :]
        burn_index = ds_bi1['burning_index_g'][day_idx, :, :]

    # Sample data for visualization
    max_temp_sample = max_temp[::sample_factor, ::sample_factor]
    dead_fuel_moisture_sample = dead_fuel_moisture[::sample_factor, ::sample_factor]
    burn_index_sample = burn_index[::sample_factor, ::sample_factor]

    # Plot filled contours for dead fuel moisture on the first subplot
    contour = ax_contour.contourf(lon, lat, dead_fuel_moisture_sample, levels=10, cmap="summer", alpha=0.6, extend="both")

    # Plot contour lines for temperature on the first subplot
    temp_contour = ax_contour.contour(lon, lat, max_temp_sample, cmap='Reds', levels=10, linewidths=1.5)

     # Plot burning index as scatter plot on the second subplot
    scatter = ax_scatter.scatter(lon_grid, lat_grid, c=burn_index_sample, s=20, cmap="hot", marker="o", alpha=0.6)

    # Add color bar for dead fuel moisture (only create it once)
    if dfm_cbar is None:
        dfm_cbar = fig.colorbar(contour, ax=ax_contour, label="Dead Fuel Moisture (%)")

    # Add color bar for burning index (only create it once)
    if bi_cbar is None:
        bi_cbar = fig.colorbar(scatter, ax=ax_scatter, label="Burning Index (BI)")

    # Color for the contour lines(max_temp)
    if temp_cbar is None:
        temp_cbar = fig.colorbar(temp_contour, ax=ax_contour, label="Max Temperature(K)")
    # Set titles and labels
    ax_contour.set_title("Dead Fuel Moisture " + idxtodate(day_idx)+ "\nContour Lines: Max Temperature (K)")
    ax_contour.set_xlabel("Longitude")
    ax_contour.set_ylabel("Latitude")

    ax_scatter.set_title("Burning Index\n" + idxtodate(day_idx))
    ax_scatter.set_xlabel("Longitude")
    ax_scatter.set_ylabel("Latitude")

# Set up FuncAnimation
ani = FuncAnimation(fig, update, frames=days_indices, repeat=True)

# Save the animation as a GIF
ani.save("fire_danger_analysis_side_by_side.gif", writer='pillow', fps=1)

plt.close(fig)  # Close the figure when done

"""# Flood Potential Analysis
**Variables:**  Precipitation Accumulation, etr, and Wind Speed

**Inference:** Areas with heavy precipitation and low etr indicates high soil water saturation causing higher runoff potential, thereby increasing flood risk. Wind speed also affects evapotranspiration, influencing soil moisture. So low wind speed also increase flood potential.

**Visualization:**
*   Contour Lines: Precipitation Accumulation.
*   Filled Contours: etr.
*   Overlay: wind speed vectors.
"""

import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from datetime import datetime, timedelta

# Load datasets
ds_pr1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/pr_2023.nc')  # precipitation accumulation dataset
ds_pr2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/pr_2024.nc')  # precipitation accumulation dataset
ds_etr1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/etr_2023.nc')    # evotranspiration dataset
ds_etr2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/etr_2024.nc')    # evotranspiration dataset
ds_wind1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/vs_2023.nc')  # Wind velocity dataset
ds_wind2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/vs_2024.nc')  # Wind velocity dataset
ds_th1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/th_2023.nc')  # Wind direction dataset (assumes u and v components)
ds_th2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/th_2024.nc')  # Wind direction dataset (assumes u and v components)

# Select the 9 days for the animation (adjust indices as needed)
# days_indices = np.linspace(0, len(ds_tmmx['day']) - 1, 9, dtype=np.float64).astype(int)
day_indices = [310,321,336,341,352,364,7,18,31]
# Sampling factor to reduce grid size for visualization
sample_factor = 18

# Sample latitude and longitude grids
lat = ds_pr2['lat'][::sample_factor]
lon = ds_pr2['lon'][::sample_factor]

# Create figure and initial plot
# Initialize wind plot (quiver) variables
# fig, ax = plt.subplots(figsize=(10, 6))

fig, axes = plt.subplots(1, 2, figsize=(16, 6), constrained_layout = True)
ax_contour, ax_quiver = axes
etr_cbar = pr_cbar = quiver_cbar = None

norm = Normalize(vmin=0, vmax=10)

def idxtodate(day_idx):
    if(day_idx<300):
        start_date = datetime(2024, 1, 1)
    else:
        start_date = datetime(2023, 1, 1)

    target_date = start_date + timedelta(days=day_idx - 1)
    return target_date.strftime("%Y-%m-%d")

def update(day_idx):
    global etr_cbar, quiver_cbar, pr_cbar

    ax_contour.cla()
    ax_quiver.cla()

    # Get temperature, humidity, and wind data for the specific day
    if(day_idx<300):
        ppt_amt = ds_pr2['precipitation_amount'][day_idx, :, :]
        etr = ds_etr2['potential_evapotranspiration'][day_idx, :, :]
        u_wind = ds_wind2['wind_speed'][day_idx, :, :]  # Assuming wind dataset has 'u_component'
        v_dir = ds_th2['wind_from_direction'][day_idx, :, :]  # and 'v_component' for wind velocity

    else:
        ppt_amt = ds_pr1['precipitation_amount'][day_idx, :, :]
        etr = ds_etr1['potential_evapotranspiration'][day_idx, :, :]
        u_wind = ds_wind1['wind_speed'][day_idx, :, :]  # Assuming wind dataset has 'u_component'
        v_dir = ds_th1['wind_from_direction'][day_idx, :, :]  # and 'v_component' for wind velocity


    # Sample data for visualization
    ppt_amt_sample = ppt_amt[::sample_factor, ::sample_factor]
    etr_sample = etr[::sample_factor, ::sample_factor]
    speed_sample = u_wind[::sample_factor, ::sample_factor]
    v_dir_sample = v_dir[::sample_factor, ::sample_factor]

    #calculate u nad v components for the quiver plot
    U = speed_sample * np.cos(np.radians(270 - v_dir_sample))
    V = speed_sample * np.sin(np.radians(270 - v_dir_sample))

    magnitude = np.sqrt(U**2 + V**2)
    u_wind_norm = U / magnitude
    v_wind_norm = V / magnitude

    # Plot filled contours for relative humidity
    contour = ax_contour.contourf(lon, lat, etr_sample, levels=20, cmap="YlGnBu", alpha=0.7, extend="both")

    # Plot contour lines for temperature
    pr_contour = ax_contour.contour(lon, lat, ppt_amt_sample, cmap='Reds_r', levels=10, linewidths=1.5)
    # plt.clabel(pr_contour, inline=True, fontsize=10, fmt='%1.0f°C')

    # Add wind velocity as arrows (quiver plot)
#     quiver = ax_quiver.quiver(lon, lat, u_wind_norm, v_wind_norm,speed_sample, cmap='viridis', scale=100, color='purple', alpha=0.7)
    # quiver = ax.quiver(lon, lat, u_wind_norm, v_wind_norm,speed_sample, cmap='viridis', scale=100, alpha=0.7)
    quiver = ax_quiver.quiver(
        lon_grid, lat_grid, U, V, speed_sample,
        cmap='viridis', scale=200, norm=norm, alpha=1
    )
    # Add color bar for humidity (only create it once)
    if etr_cbar is None:
        etr_cbar = fig.colorbar(contour, ax=ax_contour, label="Evapotranspiration (mm)")

    if quiver_cbar is None:
        quiver_cbar = fig.colorbar(quiver, ax=ax_quiver, label="Wind Speed (m/s)")

    if pr_cbar is None:
        pr_cbar = fig.colorbar(pr_contour, ax=ax_contour, label="Precipitation Amount (mm)")

    # Update title to reflect current day index
    ax_contour.set_title("Flood Potential Analysis - "+  idxtodate(day_idx) + "\nContour Lines: Precipitation (mm)")
    ax_contour.set_xlabel("Longitude")
    ax_contour.set_ylabel("Latitude")

    ax_quiver.set_title("Wind Speed and Direction\n" + idxtodate(day_idx))
    ax_quiver.set_xlabel("Longitude")
    ax_quiver.set_ylabel("Latitude")

# Set up FuncAnimation
ani = FuncAnimation(fig, update, frames=day_indices, repeat=True)

# Save the animation as a GIF
ani.save("flood_potential_analysis.gif", writer='pillow', fps=1)

plt.close(fig)  # Close the figure when done

"""# Agricultural Stress
**Variables:** Maximum Temperature, Precipitation, and Relative Humidity.
**Inference**: High temperatures, low precipitation, and low humidity can create stress conditions for crops. Monitoring these factors can help in determining areas at risk of crop yield reduction.
**Visualization**:
*   Contour Lines: Maximum Temperature.
*   Filled Contours: Precipitation accumulation.
*   Overlay: Humidity as color-coded points.
"""

import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from datetime import datetime, timedelta

# Load datasets
ds_temp1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/tmmx_2023.nc')        # Maximum temperature dataset
ds_temp2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/tmmx_2024.nc')        # Maximum temperature dataset
ds_pr1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/pr_2023.nc')    # Precipitation dataset
ds_pr2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/pr_2024.nc')    # Precipitation dataset
ds_hum1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/rmin_2023.nc') # Relative humidity dataset
ds_hum2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/rmin_2024.nc') # Relative humidity dataset

# Select days for the animation (adjust indices as needed)
days_indices = [310, 321, 336, 341, 352, 364, 7, 18, 31]
sample_factor = 18  # Sampling factor to reduce grid size for visualization

# Sample latitude and longitude grids
lat = ds_temp2['lat'][::sample_factor]
lon = ds_temp2['lon'][::sample_factor]
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Initialize figure
# fig, ax = plt.subplots(figsize=(10, 6))
fig, axes = plt.subplots(1,2, figsize=(16, 6),constrained_layout=True)
ax_contour, ax_scatter = axes
pr_cbar = hm_cbar = temp_cbar = None

def idxtodate(day_idx):
    """Convert day index to date for labeling purposes."""
    if day_idx < 300:
        start_date = datetime(2024, 1, 1)
    else:
        start_date = datetime(2023, 1, 1)
    target_date = start_date + timedelta(days=day_idx - 1)
    return target_date.strftime("%Y-%m-%d")

def update(day_idx):
    global pr_cbar, hm_cbar, temp_cbar
    ax_scatter.cla()
    ax_contour.cla()

    # Extract daily data
    if(day_idx < 300):
        max_temp = ds_temp2['air_temperature'][day_idx, :, :]
        precipitation = ds_pr2['precipitation_amount'][day_idx, :, :]
        humidity = ds_hum2['relative_humidity'][day_idx, :, :]
    else:
        max_temp = ds_temp1['air_temperature'][day_idx, :, :]
        precipitation = ds_pr1['precipitation_amount'][day_idx, :, :]
        humidity = ds_hum1['relative_humidity'][day_idx, :, :]

    # Sample data for visualization
    max_temp_sample = max_temp[::sample_factor, ::sample_factor]
    precipitation_sample = precipitation[::sample_factor, ::sample_factor]
    humidity_sample = humidity[::sample_factor, ::sample_factor]

    # Contour lines for maximum temperature
    temp_contour = ax_contour.contour(lon, lat, max_temp_sample, levels=10, cmap="Reds", linewidths=1.5)
#     temp_contour.collections[0].set_label("Max Temperature (K)")  # Label for the legend

    # Filled contours for precipitation
    pr_contour = ax_contour.contourf(lon, lat, precipitation_sample, levels=10, cmap="coolwarm", alpha=0.7, extend="both")

    # Scatter points for relative humidity
    humidity_scatter = ax_scatter.scatter(lon_grid, lat_grid, c=humidity_sample, cmap="winter", s=20, marker="o", alpha=0.4)

    # Add color bar for precipitation (only create it once)
    if pr_cbar is None:
        pr_cbar = fig.colorbar(pr_contour, ax=ax_contour, label="Precipitation Accumulation (mm)")

    # Add color bar for relative humidity
    if hm_cbar is None:
        hm_cbar = fig.colorbar(humidity_scatter, ax=ax_scatter, label="Relative Humidity (%)")

    #add color bar for max temp
    if temp_cbar is None:
        temp_cbar = fig.colorbar(temp_contour, ax=ax_contour, label="Max Temperature (K)")

    # Update title with date and label contour lines for max temp
    ax_contour.set_title("Agricultural Stress Analysis - " + idxtodate(day_idx) + "\nContour Lines: Max Temperature (K)")
    ax_contour.set_xlabel("Longitude")
    ax_contour.set_ylabel("Latitude")

    ax_scatter.set_title("Relative Humidity - " + idxtodate(day_idx))
    ax_scatter.set_xlabel("Longitude")
    ax_scatter.set_ylabel("Latitude")

# Set up FuncAnimation
ani = FuncAnimation(fig, update, frames=days_indices, repeat=True)

# Save the animation as a GIF
ani.save("agricultural_stress_analysis.gif", writer='pillow', fps=1)

plt.close(fig)  # Close figure when done

"""Radiation and Precipitation
Variables: Downward surface shortwave radiation and precipitation accumulation.
Inference: This combination helps to assess solar energy inputs versus moisture availability. For instance, high radiation with low precipitation can indicate drought-prone areas or zones with high evapotranspiration potential, which is critical for agricultural planning.

# Evapotranspiration Stress
Variables: Downward Surface Shortwave Radiation, Reference Evapotranspiration (ET0), and Wind Velocity.
Inference: High solar radiation and wind speed can increase evapotranspiration, impacting water demand for plants and agriculture. Areas with high ET0 might require increased irrigation.
Visualization:
Contour Lines: Downward Shortwave Radiation.
Filled Contours: Evapotranspiration (ET0).
Overlay: Wind Velocity vectors.
"""

import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from datetime import datetime, timedelta

# Load datasets
ds_rad1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/srad_2023.nc')      # Downward Surface Shortwave Radiation dataset
ds_rad2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/srad_2024.nc')      # Downward Surface Shortwave Radiation dataset
ds_et1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/etr_2023.nc')         # Reference Evapotranspiration (ET0) dataset
ds_et2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/etr_2024.nc')         # Reference Evapotranspiration (ET0) dataset
ds_wind1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/vs_2023.nc')      # Wind Velocity dataset
ds_wind2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/vs_2024.nc')      # Wind Velocity dataset
ds_dir2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/th_2024.nc')      # Wind direction dataset
ds_dir1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/th_2023.nc')      # Wind direction dataset

# Select days for the animation (adjust indices as needed)
days_indices = [310, 321, 336, 341, 352, 364, 7, 18, 31]
sample_factor = 18  # Sampling factor to reduce grid size for visualization

# Sample latitude and longitude grids
lat = ds_rad2['lat'][::sample_factor]
lon = ds_rad2['lon'][::sample_factor]
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Initialize figure

fig, axes = plt.subplots(1, 2, figsize=(16, 6), constrained_layout = True)
ax_contour, ax_vector = axes
rad_cbar = wind_cbar = et_cbar = None

norm = Normalize(vmin=0, vmax=10)

def idxtodate(day_idx):
    """Convert day index to date for labeling purposes."""
    if day_idx < 300:
        start_date = datetime(2024, 1, 1)
    else:
        start_date = datetime(2023, 1, 1)
    target_date = start_date + timedelta(days=day_idx - 1)
    return target_date.strftime("%Y-%m-%d")

def update(day_idx):
#     global rad_contour, et_contour, wind_vectors, wind_cbar, et_cbar, rad_cbar

    global rad_cbar , wind_cbar , et_cbar
    ax_contour.cla()
    ax_vector.cla()

    # Extract daily data
    if(day_idx < 300):
        radiation = ds_rad2['surface_downwelling_shortwave_flux_in_air'][day_idx, :, :]#check for this variable
        evapotranspiration = ds_et2['potential_evapotranspiration'][day_idx, :, :]
        wind_speed = ds_wind2['wind_speed'][day_idx, :, :]
        wind_dir = ds_dir2['wind_from_direction'][day_idx, :, :]
    else:
        radiation = ds_rad1['surface_downwelling_shortwave_flux_in_air'][day_idx, :, :]
        evapotranspiration = ds_et1['potential_evapotranspiration'][day_idx, :, :]
        wind_speed = ds_wind1['wind_speed'][day_idx, :, :]
        wind_dir = ds_dir1['wind_from_direction'][day_idx, :, :]

    # Sample data for visualization
    rad_sample = radiation[::sample_factor, ::sample_factor]
    et_sample = evapotranspiration[::sample_factor, ::sample_factor]
    speed_sample = wind_speed[::sample_factor, ::sample_factor]
    wind_dir_sample = wind_dir[::sample_factor, ::sample_factor]

    #calculate u nad v components for the quiver plot
    U = speed_sample * np.cos(np.radians(270 - wind_dir_sample))
    V = speed_sample * np.sin(np.radians(270 - wind_dir_sample))

    magnitude = np.sqrt(U**2 + V**2)
    u_wind_norm = U / magnitude
    v_wind_norm = V / magnitude


    # Contour lines for downward shortwave radiation
    rad_contour = ax_contour.contour(lon_grid, lat_grid, rad_sample, levels=10, cmap="YlOrBr", linewidths=1.5)
    rad_contour.collections[0].set_label("Downward Shortwave Radiation (W/m²)")  # Label for the legend

    # Filled contours for evapotranspiration (ET0)
    et_contour = ax_contour.contourf(lon_grid, lat_grid, et_sample, levels=10, cmap="coolwarm", alpha=0.7, extend="both")

    # Vector overlay for wind velocity
#     wind_vectors = ax_vector.quiver(lon_grid, lat_grid, u_wind_norm, v_wind_norm, speed_sample,cmap='viridis', color="purple", scale=500, alpha=0.6)
    #  quiver = ax_quiver.quiver(lon, lat, u_wind_norm, v_wind_norm,speed_sample, cmap='viridis', scale=100, color='purple', alpha=0.7)
    wind_vectors = ax_vector.quiver(
        lon_grid, lat_grid, U, V, speed_sample,
        cmap='viridis', scale=200, norm=norm, alpha=1
    )
    ax_quiver.set_title("Wind Speed and Direction")
    ax_quiver.set_xlabel("Longitude")
    ax_quiver.set_ylabel("Latitude")
    # Add color bar for evapotranspiration (only create it once)
    if et_cbar is None:
        et_cbar = fig.colorbar(et_contour, ax=ax_contour, label="Evapotranspiration (ETR) (mm/day)")
    # Add color bar for wind (only create it once)
    if wind_cbar is None:
        wind_cbar = fig.colorbar(wind_vectors, ax=ax_vector, label="wind Speed (m/s)")
    #add color bar for contour lines(downward shortwave Radiation)
    if rad_cbar is None:
        rad_cbar = fig.colorbar(rad_contour, ax=ax_contour, label="Downward Shortwave Radiation (W/m²)")

    # Update titles and labels
    ax_contour.set_title("Evotranspiration Stress Analysis - " + idxtodate(day_idx) + "\nContour Lines: Downward Shortwave Radiation (W/m²)")
    ax_contour.set_xlabel("Longitude")
    ax_contour.set_ylabel("Latitude")

    ax_vector.set_title("Wind Velocity & Direction - " + idxtodate(day_idx))
    ax_vector.set_xlabel("Longitude")
    ax_vector.set_ylabel("Latitude")

# Set up FuncAnimation
ani = FuncAnimation(fig, update, frames=days_indices, repeat=True)

# Save the animation as a GIF
ani.save("EvoTranspiration_stress_analysis.gif", writer='pillow', fps=1)

plt.close(fig)  # Close figure when done

"""# Cold Wave Detection
**Variables**: Minimum Temperature, Wind Speed, and Specific Humidity.
**Inference**: Extremely low temperatures combined with high wind speeds and low humidity are indicative of cold waves. This is useful for cold-weather alerts in populated or vulnerable areas.
**Visualization**:
Contour Lines: Minimum Temperature.
Filled Contours: Specific humidity.
Overlay: Wind speed and dirction as quiverplot.
"""

import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from datetime import datetime, timedelta
from matplotlib.colors import Normalize

# Load datasets
ds_temp_min1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/tmmn_2023.nc')
ds_temp_min2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/tmmn_2024.nc')
ds_humidity1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/sph_2023.nc')
ds_humidity2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/sph_2024.nc')
ds_wind1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/vs_2023.nc')
ds_wind2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/vs_2024.nc')
ds_dir1 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/th_2023.nc')
ds_dir2 = xr.open_dataset('/kaggle/input/gridmet-dataset/netCDF4_datasets/th_2024.nc')

# Select days and sample factor for down-sampling
days_indices = [310, 321, 336, 341, 352, 364, 7, 18, 31]
sample_factor = 18
lat = ds_temp_min2['lat'][::sample_factor]
lon = ds_temp_min2['lon'][::sample_factor]
lon_grid, lat_grid = np.meshgrid(lon, lat)

# Initialize figure
fig, axes = plt.subplots(1, 2, figsize=(16, 6), constrained_layout = True)
ax_contour, ax_quiver = axes
cbar_temp = cbar_humidity = cbar_quiver = None

# Set up normalization for consistent wind speed color scaling
norm = Normalize(vmin=0, vmax=10)

def idxtodate(day_idx):
    """Convert day index to date for labeling purposes."""
    if day_idx < 300:
        start_date = datetime(2024, 1, 1)
    else:
        start_date = datetime(2023, 1, 1)
    target_date = start_date + timedelta(days=day_idx - 1)
    return target_date.strftime("%Y-%m-%d")

def update(day_idx):
    global cbar_temp, cbar_humidity, cbar_quiver
#       global cbar_temp, cbar_humidity, cbar_quiver, ax_contour, ax_quiver
    # Clear previous plots
    ax_contour.cla()
    ax_quiver.cla()

    # Extract daily data
    if day_idx < 300:
        temp_min = ds_temp_min2['air_temperature'][day_idx, :, :]
        humidity = ds_humidity2['specific_humidity'][day_idx, :, :]
        speed = ds_wind2['wind_speed'][day_idx, :, :]
        wind_dir = ds_dir2['wind_from_direction'][day_idx, :, :]
    else:
        temp_min = ds_temp_min1['air_temperature'][day_idx, :, :]
        humidity = ds_humidity1['specific_humidity'][day_idx, :, :]
        speed = ds_wind1['wind_speed'][day_idx, :, :]
        wind_dir = ds_dir1['wind_from_direction'][day_idx, :, :]

    # Down-sample for visualization
    temp_min_sample = temp_min[::sample_factor, ::sample_factor]
    humidity_sample = humidity[::sample_factor, ::sample_factor]
    speed_sample = speed[::sample_factor, ::sample_factor]
    wind_dir_sample = wind_dir[::sample_factor, ::sample_factor]

    # Calculate U and V components for wind vectors
    U = speed_sample * np.cos(np.radians(270 - wind_dir_sample))
    V = speed_sample * np.sin(np.radians(270 - wind_dir_sample))

    # Plot contour of minimum temperature
    temp_contour = ax_contour.contour(lon, lat, temp_min_sample, levels=10, cmap="Blues", linewidths=1.5)
#     temp_contour = ax_contour.contour(lon, lat, temp_min_sample, levels=10, colors="blue", linewidths=1.5)
#     plt.clabel(temp_contour, inline=True, fontsize=10, fmt='%1.0fK')
    ax_contour.set_title(f"Cold Wave Detection - {idxtodate(day_idx)}\nContour Lines: Min Temperature (K)")
    ax_contour.set_xlabel("Longitude")
    ax_contour.set_ylabel("Latitude")

    # Plot filled contour for specific humidity
    humidity_contour = ax_contour.contourf(lon, lat, humidity_sample, levels=10, cmap="YlGnBu", alpha=0.7, extend="both")
    # Plot wind vectors with color mapped by speed
    quiver = ax_quiver.quiver(
        lon_grid, lat_grid, U, V, speed_sample,
        cmap='viridis', scale=200, norm=norm, alpha=0.7
    )
    ax_quiver.set_title("Wind Speed and Direction")
    ax_quiver.set_xlabel("Longitude")
    ax_quiver.set_ylabel("Latitude")

    # Color bars (added only once)
    if cbar_humidity is None:
        cbar_humidity = fig.colorbar(humidity_contour, ax=ax_contour, label="Specific Humidity (kg/kg)")
    if cbar_temp is None:
        cbar_temp = fig.colorbar(temp_contour, ax=ax_contour, label="Minimum Temperature (K)")
    if cbar_quiver is None:
        cbar_quiver = fig.colorbar(quiver, ax=ax_quiver, label="Wind Speed(m/s)")

# Set up animation
ani = FuncAnimation(fig, update, frames=days_indices, repeat=True)
ani.save("cold_wave_detection.gif", writer='pillow', fps=1)
plt.close(fig)