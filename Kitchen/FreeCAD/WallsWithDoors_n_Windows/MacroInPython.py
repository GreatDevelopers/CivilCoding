import FreeCAD, Draft, Arch
import csv

DEBUG = False  # Global flag for enabling/disabling debugging

def create_walls_from_csv(filepath):
    """Creates walls and doors/windows from structured CSV data with optional debugging."""
    
    global DEBUG
    print("\n--- Starting Wall & Opening Creation ---\n")

    try:
        with open(filepath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

            if not rows:
                print("❌ Error: CSV file is empty.")
                return

            print("✅ CSV file loaded successfully.\n")

            i = 0
            while i < len(rows):
                row = rows[i]

                # ✅ **Check for empty rows before accessing `row[0]`**
                if not row or len(row) == 0:  
                    if DEBUG: print(f"⚠️  Skipping completely empty row at {i+1}.")
                    i += 1
                    continue

                print(f"🔍 Processing Row {i+1}: {row}")  # Debug log for each row

                # Check for debugging mode
                if row[0].strip().lower() == "debugging":
                    if len(row) > 1 and row[1].strip().lower() in ["y", "yes"]:
                        DEBUG = True
                        print("🛠️  Debugging Mode Enabled 🛠️")
                    else:
                        DEBUG = False
                    i += 1
                    continue

                # Skip comment lines
                if row[0].startswith("#"):  
                    if DEBUG: print(f"🔹 Skipping comment at row {i+1}.")
                    i += 1
                    continue

                if row[0].strip().lower() == "walllabel":  # Skip main headers
                    if DEBUG: print(f"🔹 Skipping main header row at {i+1}.")
                    i += 1
                    continue

                if row[0] == "":  # Door/window header or entry
                    if len(row) < 7:
                        print(f"⚠️ Skipping incomplete door/window row at {i+1}: {row}")
                        i += 1
                        continue

                    if "doorWindowLabel" in row:  # Secondary header for openings
                        if DEBUG: print(f"🔹 Skipping door/window header row at {i+1}.")
                    else:
                        if DEBUG: print(f"⚠️ Unexpected blank first column at row {i+1}: {row}")
                    i += 1
                    continue

                # If a new wall starts
                if row[0].strip():  
                    if len(row) < 8:
                        print(f"❌ Error: Insufficient data for wall at row {i+1}. Skipping...")
                        i += 1
                        continue

                    print(f"\n🔹 Creating Wall: {row[0]}")
                    current_wall = create_wall(row)
                    i += 1  

                    # Process associated doors/windows
                    while i < len(rows) and rows[i] and rows[i][0] == "":
                        if DEBUG: print(f"   ➡ Processing door/window at Row {i+1}: {rows[i]}")
                        create_door_window(rows[i], current_wall)
                        i += 1  

                    # Move and orient the wall after all doors/windows are created
                    reposition_wall(current_wall, row)

                else:
                    if DEBUG: print(f"⚠️  Unexpected blank first column at row {i+1}. Skipping...")
                    i += 1  
    
    except FileNotFoundError:
        print(f"❌ Error: File not found at {filepath}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

    print("\n✅ Wall & Opening Creation Completed!\n")

def create_wall(row):
    """Creates a wall in FreeCAD."""
    try:
        label, x, y, z, angle, length, width, height = row
        x, y, z, angle, length, width, height = map(float, [x, y, z, angle, length, width, height])

        p1 = FreeCAD.Vector(0, 0, 0)
        p2 = FreeCAD.Vector(length, 0, 0)
        baseline = Draft.makeLine(p1, p2)
        wall = Arch.makeWall(baseline, length=None, width=width, height=height, align="Right")

        wall.Label = label

        if DEBUG: print(f"   ✅ Wall Created: {label} at ({x}, {y}, {z}) with angle {angle}°")
        
        FreeCAD.ActiveDocument.recompute()
        return wall
    except Exception as e:
        print(f"❌ Error creating wall '{row[0]}': {e}")
        return None

def create_door_window(row, wall):
    """Creates a door/window in FreeCAD and attaches it to a wall."""
    try:
        _, label, type, width, height, x, z = row
        width, height, x, z = map(float, [width, height, x, z])

        base = FreeCAD.Vector(x, 0, z)
        axis = FreeCAD.Vector(1, 0, 0)
        place = FreeCAD.Placement(base, FreeCAD.Rotation(axis, 90))

        door_window = Arch.makeWindowPreset(
            type, width=width, height=height, h1=100, h2=100, h3=100, w1=200, w2=100, o1=0, o2=100, placement=place
        )

        door_window.Label = label
        door_window.Hosts = [wall]

        if DEBUG: print(f"   ✅ {type} '{label}' added at ({x}, 0, {z}) to Wall: {wall.Label}")
        
        FreeCAD.ActiveDocument.recompute()
    except Exception as e:
        print(f"❌ Error creating {row[1]}: {e}")

def reposition_wall(wall, row):
    """Moves and rotates the wall to its final position."""
    try:
        _, x, y, z, angle, _, _, _ = row
        x, y, z, angle = map(float, [x, y, z, angle])

        wall.Placement = FreeCAD.Placement(FreeCAD.Vector(x, y, z), FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), angle))
        FreeCAD.ActiveDocument.recompute()

        if DEBUG: print(f"   🔄 Wall '{wall.Label}' repositioned to ({x}, {y}, {z}) with {angle}° rotation")
    except Exception as e:
        print(f"❌ Error repositioning wall '{wall.Label}': {e}")

# Example usage
csv_file_path = "/home/hsrai/FreeCAD/data.csv"  # Replace with your CSV file path
create_walls_from_csv(csv_file_path)
print(f"\n🔹 Macro execution is over: Good CSV\n")
