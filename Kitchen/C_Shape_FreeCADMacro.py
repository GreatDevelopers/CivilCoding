import FreeCAD as App
import FreeCADGui as Gui
import Part

# Clear the document
doc = App.newDocument("Kitchen")

# Unit conversion
FT = 304.8
IN = 25.4

# Kitchen dimensions
kitchen_width = 10.875 * FT  # 10' 10.5"
kitchen_length = 14 * FT  # 14'
kitchen_height = 10.25 * FT  # 10' 3"
wall_thickness = 9 * IN  # 9-inch walls

# Countertop
counter_height = 2.75 * FT  # 2' 9"
counter_depth = 2 * FT  # 2'
counter_thickness = 30 + 2 * IN # 30 mm thick granite

# Wall cabinet
wall_cabinet_height = 2.5 * FT # 2' 6"
wall_cabinet_depth = 1.5 * FT  # 1' 6"
wall_cabinet_top = 7 * FT  # 7' from floor

# Base cabinet
base_cabinet_height = counter_height - counter_thickness
base_cabinet_depth = counter_depth

# Appliances
fridge_width = 2.33 * FT
fridge_depth = 2.25 * FT
stove_width = 24 * IN
stove_depth = 20 * IN
sink_width = 3 * FT
dishwasher_width = 2 * FT
microwave_width = 2 * FT
microwave_depth = 1 * FT
food_processor_width = 1.5 * FT
food_processor_depth = 16 * IN
chimney_width = stove_width
chimney_depth = counter_depth
chimney_height = 6 * IN

# Door
door_width = 3.5 * FT
door_height = 7 * FT

# Window1
win1_width = 2.5 * FT
win1_height = 1.75 * FT

# Window2
win2_width = 4 * FT + 4.5*IN
win2_height = 4.25 * FT


# Function to create a box
def create_box(x, y, z, length, width, height, name, color):
    obj = doc.addObject("Part::Box", name)
    obj.Placement.Base = App.Vector(x, y, z)
    obj.Length = length
    obj.Width = width
    obj.Height = height
    obj.ViewObject.ShapeColor = tuple(float(c) for c in color)
    return obj

# Walls
create_box(0, -7*FT, 0, wall_thickness, kitchen_length + wall_thickness + 7*FT, kitchen_height, "Wall_Long1", (0.8, 0.8, 0.8))
create_box(kitchen_width + wall_thickness, 0, 0, wall_thickness, kitchen_length + wall_thickness, kitchen_height, "Wall_Long2", (0.8, 0.8, 0.8))
create_box(wall_thickness, 0, 7*FT, kitchen_width, wall_thickness, 3.25*FT, "Wall_Short1", (0.8, 0.8, 0.8))
create_box(wall_thickness, kitchen_length, 0, kitchen_width, wall_thickness, kitchen_height, "Wall_Short2", (0.8, 0.8, 0.8))

# Countertop
create_box(wall_thickness, kitchen_length - counter_depth, base_cabinet_height, kitchen_width - door_width - sink_width, counter_depth, counter_thickness, "CountertopShortBack", (0, 0.5, 0))
create_box(wall_thickness + counter_depth, 0, base_cabinet_height, kitchen_width - door_width - counter_depth - 1.5*FT, counter_depth, counter_thickness, "CountertopShortFront", (0, 0.5, 0))
create_box(wall_thickness, 0, base_cabinet_height, counter_depth, kitchen_length - counter_depth, counter_thickness, "CountertopLong", (0, 0.5, 0))

# Base cabinets
create_box(wall_thickness, kitchen_length - counter_depth, 0, kitchen_width - door_width, counter_depth, base_cabinet_height, "BaseCabinetShort", (0, 0.5, 0))
create_box(wall_thickness + counter_depth, 0, 0, kitchen_width - door_width - counter_depth - 1.5*FT, counter_depth, base_cabinet_height, "BaseCabinetShortFront", (0, 0.5, 0))
create_box(wall_thickness, 0, 0, counter_depth, kitchen_length - counter_depth, base_cabinet_height, "BaseCabinetLong", (0, 0.5, 0))

# Wall cabinets along long wall
create_box(wall_thickness, 0, wall_cabinet_top - wall_cabinet_height, wall_cabinet_depth, 6.5*FT, wall_cabinet_height, "WallCabL1", (0, 0.5, 0))
create_box(wall_thickness, (8.5) * FT, wall_cabinet_top - wall_cabinet_height, wall_cabinet_depth, (3.75 + 2.5)*FT, wall_cabinet_height, "WallCabL2", (0, 0.5, 0))

# Appliances
create_box(wall_thickness + 3 * IN, -(fridge_width + 3*FT), 0, fridge_depth, fridge_width, 5.5 * FT, "Fridge", (0.2, 0.2, 0.2))
create_box(wall_thickness + kitchen_width - door_width - sink_width, kitchen_length - counter_depth, counter_height - 100, sink_width, counter_depth, 100, "Sink", (0, 0, 1))
# RO inside cabinet under the sink
#create_box(wall_thickness + kitchen_width - door_width - 1.5 * FT, kitchen_length - 1.0 *FT, counter_height + 150, 1.5 * FT, 1.0 * FT, 2 * FT, "RO", (0, 0, 1))

create_box(wall_thickness + kitchen_width - door_width - sink_width - dishwasher_width, kitchen_length - counter_depth, 0, dishwasher_width, counter_depth, counter_height, "Dishwasher", (0, 1, 0))
create_box(wall_thickness + 4 * IN, 6.5 * FT, counter_height, stove_depth, stove_width, 100, "Stove", (1, 0, 0))
create_box(wall_thickness + 3*IN, kitchen_length - counter_depth + microwave_depth, counter_height, microwave_width, microwave_depth, 200, "Microwave", (0.5, 0, 0.5))
create_box(wall_thickness + kitchen_width - door_width - 1.5 * FT, kitchen_length - 1 * FT, counter_height + 2 * FT, 1.5 * FT, 1 * FT, 2 * FT, "RO", (0, 0, 1))
create_box(4 * IN, 10 * FT, counter_height, food_processor_depth, food_processor_width, 150, "Food Processor", (0.3, 0.2, 0.1))
create_box(wall_thickness, 6.5 * FT, 4.0 * FT + 10.0 *IN, chimney_depth, chimney_width, chimney_height, "Chimney", (0.2, 0.2, 0.2))


# Island
#create_box(wall_thickness + 5 * FT, 2.5 * FT, 0, 2.5 * FT, 6 * FT, counter_height, "Island", (1, 0.5, 0))

# Door
create_box(kitchen_width + wall_thickness - door_width, kitchen_length - 3, 0, door_width, wall_thickness, door_height, "Door", (0.7, 0.4, 0.1))

# Win1A
create_box(3, 4*FT, counter_height, wall_thickness, win1_width, win1_height, "Win1A", (0.7, 0.4, 0.1))

# Win1B
create_box(3, 4*FT + win1_width + 2*FT, counter_height, wall_thickness, win1_width,  win1_height, "Win1B", (0.7, 0.4, 0.1))

# Win2
create_box(wall_thickness + 1.5*FT, kitchen_length -3, counter_height, win2_width, wall_thickness, win2_height, "Win2", (0.7, 0.4, 0.1))


# Refresh view
Gui.activeDocument().activeView().viewIsometric()
Gui.SendMsgToActiveView("ViewFit")
Gui.activeDocument().activeView().setAnimationEnabled(False)

# Final message
print("Kitchen model updated successfully.")
