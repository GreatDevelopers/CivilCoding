import matplotlib.pyplot as plt
import numpy as np

# Kitchen dimensions
kitchen_width = 10.875  # 10'-10.5"
kitchen_length = 14  # 14'

# Appliance dimensions (Depth = 2', along X-axis)
appliance_depth = 2  # Standard counter depth
fridge_width = 2.33  # 2'4"
fridge_depth = 2.25  # 2'3"
sink_width = 3
stove_width = 23.0 / 12.0
stove_depth = 20.0 / 12.0
stove_x = 4.0 / 12.0
stove_y = 7.5 - stove_width / 2.0
dishwasher_width = 2
microwave_width = 2.0  # Typical width
microwave_depth = 1.0  # Typical width
food_processor_width = 1.5  # Typical width
food_processor_depth = 16.0/12.0  # Typical width
microwave_x = 3.0/12.0  # Typical width
microwave_y = kitchen_length - appliance_depth + 6.0/12.0  # Typical width
food_processor_x = 0.5  # Typical width
food_processor_y = microwave_y -  2.5 # Typical width


# Appliance positions along Y-axis (X=0)
door_width = 3.5
fridge_x = 3.0 / 12.0
fridge_y = 0
sink_x = kitchen_width - door_width - sink_width
sink_y = kitchen_length - appliance_depth
dishwasher_x = sink_x - dishwasher_width
dishwasher_y = sink_y
#microwave_x = appliance_depth  # Placed at the start of the counter
#microwave_y = kitchen_length - appliance_depth - microwave_width
#food_processor_x = appliance_depth  # Near microwave
#food_processor_y = microwave_y - food_processor_width - 0.5  # Below MW

# Door properties (Rotating Anti-clockwise about the right point)
door_x2, door_y2 = kitchen_width, kitchen_length  # Right hinge
door_thickness = 2  # 5x thicker than normal line
door_angle = np.radians(-20)  # Rotate 20 degrees anti-clockwise

# Compute rotated door endpoints
door_x1 = door_x2 - door_width * np.cos(door_angle)
door_y1 = door_y2 + door_width * np.sin(door_angle)

# Move island 1.5' to the right
island_x, island_y = 5, 3  # New position
island_width, island_length = 2.5, 6  # Adjusted width

# Create plot
fig, ax = plt.subplots(figsize=(8, 10))
ax.set_xlim(0, kitchen_width)
ax.set_ylim(0, kitchen_length)

# Draw kitchen boundary
ax.plot([0, kitchen_width, kitchen_width, 0, 0],
        [0, 0, kitchen_length, kitchen_length, 0], 'k-', lw=2)

# Draw Countertop along Y-axis at X = 0
ax.plot([appliance_depth, 0], [2.5, 2.5], 'b-', lw=3)
ax.plot([appliance_depth, appliance_depth], [2.5, kitchen_length - appliance_depth], 'b-', lw=3)
ax.plot([appliance_depth, kitchen_width - door_width], [kitchen_length - appliance_depth, kitchen_length - appliance_depth], 'b-', lw=3)
ax.plot([kitchen_width - door_width, kitchen_width - door_width], [kitchen_length - appliance_depth, kitchen_length], 'b-', lw=3)

# Draw Appliances (aligned along Y-axis, rotated for depth)
appliances = [
    ("Fridge", fridge_x, fridge_y, fridge_depth, fridge_width, "gray"),
    ("Sink", sink_x, sink_y, sink_width, appliance_depth, "blue"),
    ("DW", dishwasher_x,  dishwasher_y, dishwasher_width, appliance_depth, "green"),
    ("Stove", stove_x, stove_y, stove_depth, stove_width, "red"),
    ("MW", microwave_x, microwave_y, microwave_width, microwave_depth, "purple"),
    ("FP", food_processor_x, food_processor_y, food_processor_depth, food_processor_width, "brown"),
]

for name, x_pos, y_pos, xx, yy, color in appliances:
    ax.add_patch(plt.Rectangle((x_pos, y_pos), xx, yy, fc=color))
    ax.text(x_pos + xx / 2, y_pos + yy / 2, name, fontsize=10, color="white", 
            va="center", ha="center", fontweight="bold")

# Draw Island (Shifted Right by 1.5')
ax.add_patch(plt.Rectangle((island_x, island_y), island_width, island_length, fc="orange", alpha=0.7))
ax.text(island_x + island_width / 2, island_y + island_length / 2, "Island", 
        fontsize=12, color="black", va="center", ha="center", fontweight="bold")

# Draw Partially Open Door (Anti-clockwise Rotation about Right Point)
ax.plot([door_x1, door_x2], [door_y1, door_y2], 'r-', lw=door_thickness * 5)

# Display plot
ax.set_title("Kitchen Layout", fontsize=14)
ax.set_xticks(range(0, 12, 2))
ax.set_yticks(range(0, 16, 2))
ax.grid(True, linestyle="--", alpha=0.5)

# Print door coordinates
#print(f"Door Coordinates:")
#print(f"Right Endpoint (Hinge Point): ({door_x2:.2f}, {door_y2:.2f})")
#print(f"Left Endpoint (Rotated Open): ({door_x1:.2f}, {door_y1:.2f})")


plt.savefig("kitchen_layout.png", dpi=300, bbox_inches="tight")

plt.show()
