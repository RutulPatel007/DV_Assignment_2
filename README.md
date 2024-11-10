
# Quiver Plot Script

## Description
This script generates quiver plots based on wind speed and direction data. It creates plots where either the length or the color of the arrows represent the wind speed.

## Prerequisites
Ensure you have the following libraries installed:
- numpy
- matplotlib
- netCDF4
- basemap
- datetime
- imageio
- Pillow

You can install all the necessary libraries using pip:
```bash
pip install numpy matplotlib netCDF4 basemap datetime imageio Pillow
```

## Usage
1. **Set up your data paths:**
   - Update the `direction_file_path` and `speed_file_path` variables in the script to point to the appropriate datasets for the years 2023 and 2024.

2. **Run the script:**
   - You can run the script directly to generate plots for specific dates.
   - Example:
     ```bash
     python quiver.py
     ```

   - The script will generate plots for the following dates:
     - November 1st, 2023
     - November 15th, 2023
     - December 1st, 2023
     - December 15th, 2023
     - January 1st, 2024
     - January 15th, 2024
     - January 31st, 2024

3. **Generate GIFs:**
   - The script also includes functionality to create GIFs from the generated plots.
   - Ensure the `file_path` variable is set to the directory where your plots are saved.
   - Example:
     ```bash
     python quiver.py
     ```

## File Structure
- `quiver.py`: The main script file.

## Example Plots
The script will save the plots in the specified `file_path`.





# Streamline Plot Script

## Description
This script generates streamline plots based on wind speed and direction data. It creates images and compiles them into a GIF animation showing wind streamlines over time.

## Prerequisites
Ensure you have the following libraries installed:
- numpy
- xarray
- imageio
- matplotlib
- basemap
- scipy

You can install all the necessary libraries using pip:
```bash
pip install numpy xarray imageio matplotlib basemap scipy
```

## Usage
1. **Set up your data paths:**
   - Update the `dir_data2`, `speed_data2`, `dir_data1`, and `speed_data1` variables in the script to point to the appropriate datasets for the years 2023 and 2024.

2. **Run the script:**
   - You can run the script directly to generate streamline plots for specific days.
   - Example:
     ```bash
     python streamlines.py
     ```

   - The script will generate plots for the following days:
     - November 1st, 2023
     - November 11th, 2023
     - November 21st, 2023
     - December 1st, 2023
     - December 11th, 2023
     - December 21st, 2023
     - December 31st, 2023
     - January 9th, 2024
     - January 19th, 2024
     - January 29th, 2024

3. **Generate GIF:**
   - The script includes functionality to create a GIF from the generated plots.
   - Ensure the `file_path` variable is set to the directory where your plots are saved.
   - Example:
     ```bash
     python streamlines.py
     ```

## File Structure
- `streamlines.py`: The main script file.

## Example Plots
The script will save the plots in the specified directory and create a GIF animation.




# Colormap Visualization Script

## Description
This script generates colormap visualizations for various weather data variables. It creates plots for specific weather events and saves them as images.

## Prerequisites
Ensure you have the following libraries installed:
- xarray
- matplotlib
- numpy
- cartopy
- os

You can install all the necessary libraries using pip:
```bash
pip install xarray matplotlib numpy cartopy
```

## Usage
1. **Set up your data paths:**
   - Update the `load_single_weather_data` function in the script to point to the appropriate dataset paths for the year 2024.

2. **Run the script:**
   - You can run the script directly to generate colormap plots for specified weather events.
   - Example:
     ```bash
     python colormap (2).py
     ```

   - The script will generate plots for the following weather events:
     - Drought and Wildfires on specified days (153, 168, 183, 198, 213, 228)

3. **Output:**
   - The generated plots will be saved in the specified `output_dir` directory.

## File Structure
- `colormap (2).py`: The main script file.

## Example Plots
The script will save the plots in the specified directory.

# TreeMap Vizualization

There are three interactive visualizations created using D3.js. Each visualization renders data from the `athlete_events.csv` file. Follow the instructions below to interact with each dashboard.

## 1. Event Participation by Year and City 

This visualization shows a **treemap** of event participation organized by **year** and **city**. You can interact with the following features:
- **Tiling Method**: Select from `Squarify`, `Slice`, `Dice`, or `Slice-Dice` layouts.
- **Top Years Display**: Limit the number of years displayed (e.g., top 5, 10, 15, etc.).

### How to Use:
1. Open `Viz1_Event_Participation.html` in a web browser.
2. Select a tiling method from the dropdown menu.
3. Choose the number of top years to display.
4. The chart will update based on your selections.

**Main File**: `Viz1_Event_Participation.html`

---

## 2. Medal Distribution by Age Group and Sex

This visualization displays a treemap showing **medal distribution** by **age group** and **sex**. You can switch between different layout methods using the dropdown menu.

### How to Use:
1. Open `Viz3.html` in a web browser.
2. Select the desired tiling method (Squarify, Slice, Dice, or Slice-Dice).
3. The treemap will adjust to reflect your selection, displaying medal distributions by age groups and sex.

**Main File**: `Viz3.html`

---

## 3. Participation Over Time in Volleyball

This visualization tracks participation in **volleyball events** over time, grouped by countries. The layout and the number of years to display are customizable.

### How to Use:
1. Open `Viz4.html` in a web browser.
2. Choose a tiling method from the dropdown.
3. Select the number of top years to visualize.
4. The visualization will update to reflect the changes.

**Main File**: `Viz4.html`

---

## Dependencies

Each HTML file relies on D3.js for rendering the treemaps. D3.js is loaded from a CDN, so an active internet connection is required to load the visualizations.
Ensure that `athlete_events.csv` is located in the same directory as the HTML files when running them locally.

---

## Usage

1. Download the files and place them in the same directory as `athlete_events.csv`.
2. Open each HTML file in a browser to interact with the visualizations.
3. Use the dropdown menus to change the display options.



# Contour Analysis Script

This Python script loads various meteorological data files in netCDF format and displays their available variables. The script is designed to work with data such as precipitation, temperature, and humidity from different datasets, which can be used for further analysis or visualization.

## Prerequisites

The script requires Python 3 and the following Python packages:
- `netCDF4` for working with netCDF data files
- `xarray` for handling multi-dimensional arrays
- `matplotlib` for visualizations
- `numpy` for numerical operations

Install these packages via:

```bash
pip install netCDF4 xarray matplotlib numpy
```
## Usage
1. **Prepare Data Files**: Place the required netCDF files (e.g., sph_2023.nc, pr_2024.nc) in the script’s directory, or update the file paths in the script if they are stored elsewhere.
2. **Run the Script**: Execute the script to load each netCDF dataset and list available variables within each file. This will help verify the structure and contents of each dataset for further analysis or plotting.
 ```bash
python contour.py
```
3. **Viewing Variables**: The script will print the variables in each dataset to the console, allowing you to inspect the specific parameters contained within each netCDF file.

## Modifying for Contour Plots
To add contour plots, identify relevant variables (e.g., lat, lon, temperature) and use **matplotlib.pyplot.contour()** for visualization. Here’s an example snippet:
 ```bash
import matplotlib.pyplot as plt

# Example contour plot
data = data_sph['temperature_variable_name'][:]  # Replace with actual variable name
plt.contour(data)
plt.title("Contour Plot")
plt.show()

```
Please update the example file paths in the code if your data files are named differently or located in a different directory.
 ```bash
python contour.py
```
