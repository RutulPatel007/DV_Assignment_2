
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

