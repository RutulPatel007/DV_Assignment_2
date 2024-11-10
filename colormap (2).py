import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize, SymLogNorm, BoundaryNorm, ListedColormap
import numpy as np
from datetime import timedelta, datetime
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature

plt.switch_backend("Agg")

# Adjust the load function to use Kaggle's file path
def load_single_weather_data(variable, year="2024"):
    filename = f"/kaggle/input/gridmet-dataset/netCDF4_datasets/{variable}_{year}.nc"
#     /kaggle/input/gridmet-dataset/netCDF4_datasets/bi_2023.nc
# /kaggle/input/gridmet-dataset/netCDF4_datasets/bi_2023.nc
    try:
        return xr.open_dataset(filename)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Weather data file not found: {e.filename}")

def plot_weather_event(
    variable,
    day,
    year="2024",
    cmap="viridis",
    scale="continuous",
    parametric="global",
    output_path=None,
    title="",
    lmin=None,
    lmax=None,
    discrete_levels=None,
):
    dataset = load_single_weather_data(variable, year)
    variable_name = list(dataset.data_vars)[0]
    data_array = dataset[variable_name].values[day, :, :]
    latitudes = dataset["lat"].values
    longitudes = dataset["lon"].values

    # Determine normalization based on scale and parametric choice
    if scale == "logarithmic":
        event_data = dataset[variable_name].values[day, :, :]
        valid_data = event_data[~np.isnan(event_data)].flatten()
        valid_min, valid_max = np.nanmin(valid_data[valid_data > 0]), np.nanmax(valid_data)
        norm = SymLogNorm(linthresh=valid_min / 10, linscale=0.1, vmin=valid_min, vmax=valid_max)
    else:
        valid_min, valid_max = (
            (np.nanmin(dataset[variable_name].values), np.nanmax(dataset[variable_name].values))
            if parametric == "global"
            else (np.nanmin(data_array), np.nanmax(data_array))
        )
        if lmin is not None: valid_min = lmin
        if lmax is not None: valid_max = lmax
        norm = BoundaryNorm(np.linspace(valid_min, valid_max, discrete_levels+1) if discrete_levels else [], discrete_levels) if discrete_levels else Normalize(vmin=valid_min, vmax=valid_max)
        cmap = ListedColormap(plt.get_cmap(cmap)(np.linspace(0, 1, len(np.linspace(valid_min, valid_max, discrete_levels+1))-1))) if discrete_levels else plt.get_cmap(cmap)

    # Set up plot with Cartopy instead of Basemap
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={"projection": ccrs.LambertConformal(central_longitude=-96, central_latitude=37.5)})
    im = ax.pcolormesh(longitudes, latitudes, data_array, cmap=cmap, norm=norm, transform=ccrs.PlateCarree(), shading="auto")
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)

    cbar = plt.colorbar(im, ax=ax, label=f"{variable_name} on {title}", fraction=0.046, pad=0.04, boundaries=norm.boundaries if discrete_levels else None)
    ax.set_title(title)
    if output_path:
        plt.savefig(output_path, bbox_inches="tight", dpi=300)
        plt.close()
    else:
        plt.show()
        plt.close()

# Replace Basemap usage in event dictionary and function calls
variable_to_title = {
    "vs": "Wind Speed",
    "srad": "Solar Radiation",
    "pr": "Precipitation",
    "erc": "Energy Release Component",
    "tmmn": "Minimum Temperature",
    "tmmx": "Maximum Temperature",
    "rmax": "Relative Humidity Max",
    "rmin": "Relative Humidity Min",
    "vpd": "Vapor Pressure Deficit",
    "sph": "Specific Humidity",
    "pet": "Potential Evapotranspiration",
    "fm100": "Fuel Moisture 100hr",
    "fm1000": "Fuel Moisture 1000hr",
}

year = "2024"
output_dir = "/kaggle/working/colormap/droughts"
os.makedirs(output_dir, exist_ok=True)

event_data={
    "Drought and Wildfires":{
        153:{
            "erc":{"cmap":"viridis","scale":"discrete","parametric":"local"},
            "vpd":{"cmap":"viridis","scale":"discrete","parametric":"local"},
        },
        153
       +15:{
            "erc":{"cmap":"viridis","scale":"discrete","parametric":"local"},
            "vpd":{"cmap":"viridis","scale":"discrete","parametric":"local"},
        },
        153
       +30:{
            "erc":{"cmap":"viridis","scale":"discrete","parametric":"local"},
            "vpd":{"cmap":"viridis","scale":"discrete","parametric":"local"},
        },
        153
       +45:{
            "erc":{"cmap":"viridis","scale":"discrete","parametric":"local"},
            "vpd":{"cmap":"viridis","scale":"discrete","parametric":"local"},
        },
        153
       +60:{
            "erc":{"cmap":"viridis","scale":"discrete","parametric":"local"},
            "vpd":{"cmap":"viridis","scale":"discrete","parametric":"local"},
        },
        153
       +75:{
            "erc":{"cmap":"viridis","scale":"discrete","parametric":"local"},
            "vpd":{"cmap":"viridis","scale":"discrete","parametric":"local"},
        },
    }
}




def gd(day):
    return (datetime(2024, 1, 1) + timedelta(days=day - 1)).strftime("%d-%m-%Y")

for event, days_data in event_data.items():
    for day, variables in days_data.items():
        date = gd(day)
        for variable, settings in variables.items():
            title = f"{variable_to_title.get(variable, variable)} on {date}"
            output_filename = f"{event.replace(' ', '')}{variable.replace(' ', '')}{date.replace(' ', '_')}.png"
            output_path = os.path.join(output_dir, output_filename)
            try:
                plot_weather_event(variable, day, year, cmap=settings["cmap"], scale=settings["scale"], parametric=settings["parametric"], output_path=output_path, title=title, discrete_levels=8 if settings["scale"] == "discrete" else None)
            except (FileNotFoundError, ValueError) as e:
                print(f"Error plotting {title} for {date}: {e}")
