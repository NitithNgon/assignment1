import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

# Initialize empty lists for each column
x_values = []
y_values = []
z_upper_values = []
z_lower_values =[]

# Read the CSV file
with open('collect_peaks_results.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        if row['event_type']=="good_events" and row['direction']=="to Vibhavadi":
            if row['velocity']!="" and row['gross_vehicle_weight']!="" and row['min_widths_wheel_Ax0']!="":
                x_values.append(float(row['velocity']))  # Convert to float if necessary
                y_values.append(float(row['gross_vehicle_weight']))
                z_upper_values.append(max(float(row['max_widths_wheel_Ax0']),float(row['max_widths_wheel_Ax1'])))
                z_lower_values.append(min(float(row['min_widths_wheel_Ax0']),float(row['min_widths_wheel_Ax1'])))
                print(float(row['velocity']),float(row['max_widths_wheel_Ax0']),float(row['max_widths_wheel_Ax1']),float(row['min_widths_wheel_Ax0']),float(row['min_widths_wheel_Ax1']))

x_unique = np.unique(x_values)
y_unique = np.unique(y_values)
x_grid, y_grid = np.meshgrid(x_unique, y_unique)
# Interpolate data onto the grid
z_upper_grid = griddata((x_values, y_values), z_upper_values, (x_grid, y_grid), method='cubic')
z_lower_grid = griddata((x_values, y_values), z_lower_values, (x_grid, y_grid), method='cubic')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'black', 'white', 'gray', 'orange', 'purple', 'pink', 'brown']


for x, y, z1, z2 in zip(x_values, y_values, z_upper_values, z_lower_values):
    # Find the correct indices for each x, y pair
    x_idx = np.where(x_unique == x)[0][0]
    y_idx = np.where(y_unique == y)[0][0]
    z_upper_grid[y_idx, x_idx] = z1
    z_lower_grid[y_idx, x_idx] = z2
    

# Plotting the surface
ax.plot_surface(x_grid, y_grid, z_upper_grid, color=colors[1], alpha=0.6, rstride=5, cstride=5, edgecolor='none', label="Z2 Surface")
ax.plot_surface(x_grid, y_grid, z_lower_grid, color=colors[0], alpha=0.6, rstride=5, cstride=5, edgecolor='none', label="Z2 Surface")

# Labeling
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Surface Plot from CSV Data')

plt.show()