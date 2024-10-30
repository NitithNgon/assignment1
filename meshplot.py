import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits.mplot3d import Axes3D


# Initialize empty lists for each column
x_values = []
y_values = []
z_values1 = []
z_values2 = []
z_values3 = []
z_values4 = []

# Read the CSV file
with open('collect_peaks_results.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        if row['event_type']=="good_events":
            if row['velocity']!="" and row['gross_vehicle_weight']!="" and row['min_widths_wheel_Ax0']!="":
                x_values.append(float(row['velocity']))  # Convert to float if necessary
                y_values.append(float(row['gross_vehicle_weight']))
                z_values1.append(float(row['min_widths_wheel_Ax0']))
                z_values2.append(float(row['max_widths_wheel_Ax0']))
                z_values3.append(float(row['min_widths_wheel_Ax1']))
                z_values4.append(float(row['max_widths_wheel_Ax1']))


x_unique = np.unique(x_values)
y_unique = np.unique(y_values)
x_grid, y_grid = np.meshgrid(x_unique, y_unique)
z_grid = np.zeros_like(x_grid, dtype=float)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'black', 'white', 'gray', 'orange', 'purple', 'pink', 'brown']
c=0
for z_list in [z_values1,z_values2,z_values3,z_values4]:
    # Populate the z_grid with z values based on x, y positions
    for x, y, z in zip(x_values, y_values, z_list):
        # Find the correct indices for each x, y pair
        x_idx = np.where(x_unique == x)[0][0]
        y_idx = np.where(y_unique == y)[0][0]
        z_grid[y_idx, x_idx] = z

    # Plotting the surface
    ax.plot_surface(x_grid, y_grid, z_grid, color=colors[c], alpha=0.6, rstride=5, cstride=5, edgecolor='none', label="Z2 Surface")
    c+=1

# Labeling
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Surface Plot from CSV Data')

plt.show()