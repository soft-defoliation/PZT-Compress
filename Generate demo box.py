import json
import os
import matplotlib.pyplot as plt
import numpy as np

# Create the dimensions of the cube
axes = [5, 5, 5]

# Create data indicating whether each voxel is filled
data = np.ones(axes, dtype=bool)

# Create 3D graphics objects
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
# Creates a color array to control the color and transparency of voxels
facecolors = '#FFD65DC0'
facecolors1 = '#7A88CCC0'
edgecolors = '#7D84A6'

# Draw voxel graphics
# ax.voxels(data, facecolors=facecolors, edgecolors=edgecolors, alpha=0.8, zorder= 1)
# Create arrow direction
arrow_directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

red_count = 0
green_count = 0

red = '#9FACD3'
green = '#009300'
blue = '#E1519C'

# The file name that stores the arrow direction
arrow_directions_file = 'arrow_directions.json'

# Check whether the file exists
if os.path.exists(arrow_directions_file):
    # Reads the arrow direction from the file
    with open(arrow_directions_file, 'r') as file:
        arrow_directions = json.load(file)
else:
    # Generate a new arrow direction and save it to a file
    arrow_directions = []
    for i in range(5):
        for j in range(5):
            for k in range(5):
                if data[i, j, k]:
                    direction = np.random.uniform(-1, 1, size=3)
                    direction[2] = np.random.uniform(0, 1)
                    direction /= np.linalg.norm(direction)  # Normalized to a unit vector
                    arrow_directions.append((i, j, k, direction.tolist()))
    with open(arrow_directions_file, 'w') as file:
        json.dump(arrow_directions, file)
# Record the location of the arrow that you want to remove
arrows_to_remove = [] 

# Randomly oriented arrows are generated in the center of each square
for (i, j, k, direction) in arrow_directions:
        if data[i, j, k]:
            x = i + 0.5
            y = j + 0.5
            z = k + 0.5

            # Take the absolute value Take the absolute value
            direction_abs = np.abs(direction)

            # Normalized to a unit vector
            unit_vector = direction / np.linalg.norm(direction)

            # The component of the unit vector on each axis
            x_component = np.abs(unit_vector[0])
            y_component = np.abs(unit_vector[1])
            z_component = np.abs(unit_vector[2])

            u, v, w = direction
            arrow_length = 1

            arrow_length_x = x_component * arrow_length
            arrow_length_y = y_component * arrow_length
            arrow_length_z = z_component * arrow_length
           
            pressure = 5
           
            px1 = arrow_length * 2.7
            py1 = arrow_length * 2.8
            pz1 = arrow_length * 5.1

            #px2 = arrow_length * 14.5
            #py2 = arrow_length * 14.5

            pressure_x = float(arrow_length_x) * pressure
            pressure_y = float(arrow_length_y) * pressure
            pressure_z = float(arrow_length_z) * pressure
            
            if pressure_x > px1 or pressure_y > py1 or pressure_z > pz1:

                arrow_color = 'none'
                arrows_to_remove.append((x, y, z))
            else:
                arrow_color = 'red'

            # Draw arrow
            ax.quiver(x - u * arrow_length / 2, y - v * arrow_length / 2, z - w * arrow_length / 2,
                      u, v, w, length=arrow_length, linewidth=2, color=arrow_color, alpha=1)

            axes1 = [i + 1, j + 1, k + 1]
            data1 = np.zeros(axes, dtype=bool)
            data1[i, j, k] = True  # Creates a box at the specified location
                # When the X-axis component exceeds 30% of the arrow length, the corresponding square changes color
           
            if pressure_x > px1 or pressure_y > py1 or pressure_z > pz1:

                ax.voxels(data1, facecolors= red, edgecolors=edgecolors, alpha=0.4, zorder=1)
                green_count += 1
            else:
                ax.voxels(data1, facecolors= blue, edgecolors=edgecolors, alpha=0.4, zorder=1)
                red_count += 1
            """    
            if pressure_x > px2 or pressure_y > py2:
                ax.voxels(data1, facecolors=blue, edgecolors=edgecolors, alpha=0.5, zorder=1)
                green_count += 1
                arrows_to_remove.append((x, y, z))
            else:
                ax.voxels(data1, facecolors= green, edgecolors=edgecolors, alpha=0.5, zorder=1)
                red_count += 1
             """      
                



# Save an image of the current pressure value
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

# Set the axis label
ax.set_xlabel('x', fontdict={'fontsize': 20, 'fontname': 'Times New Roman', 'weight': 'bold'})
ax.set_ylabel('y', fontdict={'fontsize': 20, 'fontname': 'Times New Roman', 'weight': 'bold'})
ax.set_zlabel('z', fontdict={'fontsize': 20, 'fontname': 'Times New Roman', 'weight': 'bold'})

ax.xaxis.labelpad = -15  # Adjust the value as needed
ax.yaxis.labelpad = -15  # Adjust the value as needed
ax.zaxis.labelpad = -15 # Adjust the value as needed



print(f"Number of green squares：{green_count}")
print(f"Number of red squares：{red_count}")


#Hide axis scale and scale label
#ax.set_aspect('equal')
#ax.axis('off')

 # adjust elevation 和 azimuth
ax.view_init(elev=15, azim=90) 
# Display graphics
plt.show()
 
#Save image
fig.savefig(f'{pressure:.2f}.png', dpi=300)
plt.cla()  # Clear the axis content to draw the result of the next pressure value