
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
