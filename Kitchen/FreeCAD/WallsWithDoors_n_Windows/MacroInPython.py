import FreeCAD, Draft, Arch
import csv

def create_walls_from_csv(filepath):
    """Creates walls and doors/windows from data in a CSV file."""
    
    try:
        with open(filepath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                create_wall_and_doors(row)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_wall_and_doors(wall_data):
    """Creates a wall and its associated doors/windows."""
    
    # Wall Data
    wall_label = wall_data['WallLabel']
    wall_x = float(wall_data['WallX'])
    wall_y = float(wall_data['WallY'])
    wall_z = float(wall_data['WallZ'])
    wall_angle = float(wall_data['WallAngle'])
    wall_length = float(wall_data['WallLength'])
    wall_width = float(wall_data['WallWidth'])
    wall_height = float(wall_data['WallHeight'])
    door_window_data = wall_data['DoorWindowData']

    # Create the wall
    p1 = FreeCAD.Vector(0, 0, 0)
    p2 = FreeCAD.Vector(wall_length, 0, 0)
    baseline = Draft.makeLine(p1, p2)
    wall = Arch.makeWall(baseline, length=None, width=wall_width, height=wall_height, align="Right")

    # Set wall label
    wall.Label = wall_label

    FreeCAD.ActiveDocument.recompute()  # Ensure the wall is created before adding doors/windows

    # Create doors/windows
    if door_window_data:
        door_window_entries = door_window_data.split('|')
        for entry in door_window_entries:
            door_window_properties = entry.split(',')
            door_window_label = door_window_properties[0]
            door_window_type = door_window_properties[1]
            door_window_width = float(door_window_properties[2])
            door_window_height = float(door_window_properties[3])
            door_window_x = float(door_window_properties[4])
            door_window_z = float(door_window_properties[5])

            base = FreeCAD.Vector(door_window_x, 0, door_window_z)
            axis = FreeCAD.Vector(1, 0, 0)
            place = FreeCAD.Placement(base, FreeCAD.Rotation(axis, 90))

            door_window = Arch.makeWindowPreset(
                door_window_type,
                width=door_window_width,
                height=door_window_height,
                h1=100, h2=100, h3=100, w1=200, w2=100, o1=0, o2=100,
                placement=place,
            )

            # Set door/window label
            door_window.Label = door_window_label

            # Correct the assignment of the host wall
            door_window.Hosts = [wall]  # Assign the current wall, not a generic reference

            FreeCAD.ActiveDocument.recompute()  # Ensure updates take effect

    # Position and rotate the wall
    wall_placement = FreeCAD.Placement(FreeCAD.Vector(wall_x, wall_y, wall_z), FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), wall_angle))
    wall.Placement = wall_placement
    FreeCAD.ActiveDocument.recompute()  # Recompute after positioning

# Example usage
csv_file_path = "/home/hsrai/FreeCAD/data.csv"  # Replace with your csv file path
create_walls_from_csv(csv_file_path)
print(f"Macro execution is over")
