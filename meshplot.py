import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

from itertools import combinations
from typing import List
def max_min_range_less_than20_frist_edition(max_list: List[float], min_list: List[float])-> List[float]:
    max_min_range_maximum=0
    max_min_list =[0,0]
    for i in max_list:
        for j in min_list:
            if i-j > max_min_range_maximum and i-j <20:
                max_min_range_maximum=i-j
                max_min_list=[i,j]    
    return max_min_list


def max_min_range_less_than20(wheel_widths_list: List[float])-> List[float]:
    max_min_range_maximum=0
    max_min_list =[0,0]
    combinations_2_wheel_widths = [list(pair) for pair in combinations(wheel_widths_list, 2)]
    for i in combinations_2_wheel_widths:
        if max(i)-min(i) > max_min_range_maximum and max(i)-min(i) <20:
            max_min_range_maximum= max(i)-min(i)
            # print(max_min_range_maximum)
            max_min_list=i
    # print(max_min_list)
    return max_min_list


# Initialize empty lists for each column
x_values = []
y_values = []
z_upper_values = []
z_lower_values =[]

# Read the CSV file
with open('collect_peaks_results.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        if row['event_type']=="good_events":
            if row['velocity']!="" and row['gross_vehicle_weight']!="":
                
                max_list=[float(row['max_widths_wheel_Ax0']), float(row['max_widths_wheel_Ax1'])]
                min_list=[float(row['min_widths_wheel_Ax0']), float(row['min_widths_wheel_Ax1'])]
                max_min_list= max_min_range_less_than20_frist_edition(max_list,min_list)
                if max_min_list!=[0,0]:
                    z_upper_values.append(max(max_min_list))
                    z_lower_values.append(min(max_min_list))
                    x_values.append(float(row['velocity']))  # Convert to float if necessary
                    y_values.append(float(row['gross_vehicle_weight']))
                
                # wheel_widths_list=eval(row['widths_wheel'])
                # max_min_list= max_min_range_less_than20(wheel_widths_list)
                # if max_min_list !=[0,0]:
                #     z_upper_values.append(max(max_min_list))
                #     z_lower_values.append(min(max_min_list))
                #     x_values.append(float(row['velocity']))  # Convert to float if necessary
                #     y_values.append(float(row['gross_vehicle_weight']))


x_unique = np.unique(x_values)
y_unique = np.unique(y_values)
x_grid, y_grid = np.meshgrid(x_unique, y_unique)
# Interpolate data onto the grid
z_upper_grid = griddata((x_values, y_values), z_upper_values, (x_grid, y_grid), method='linear')
z_lower_grid = griddata((x_values, y_values), z_lower_values, (x_grid, y_grid), method='linear')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'black', 'white', 'gray', 'orange', 'purple', 'pink', 'brown']


for x, y, z_upper, z_lower in zip(x_values, y_values, z_upper_values, z_lower_values):
    # Find the correct indices for each x, y pair
    x_idx = np.where(x_unique == x)[0][0]
    y_idx = np.where(y_unique == y)[0][0]
    z_upper_grid[y_idx, x_idx] = z_upper
    z_lower_grid[y_idx, x_idx] = z_lower
    

# Plotting the surface
ax.plot_surface(x_grid, y_grid, z_upper_grid, color=colors[1], alpha=0.6, rstride=5, cstride=5, edgecolor='none', label="Z1 Surface")
ax.plot_surface(x_grid, y_grid, z_lower_grid, color=colors[0], alpha=0.6, rstride=5, cstride=5, edgecolor='none', label="Z2 Surface")

# Labeling
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Surface Plot from CSV Data')

plt.show()