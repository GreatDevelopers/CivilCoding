import ezdxf
import sys

# Constants
INCH = 25.4
PHL = 59.5 * INCH
PHW = 1.5 * INCH
PHH = 3 * INCH
Z_BASE = 10 * INCH
Z_OFFSET = 50 * INCH
X_TOTAL = 180 * INCH
PVW = 20
PVH = 20
PVL = 71 * INCH
Z_BOTTOM = 1 * INCH
EDGE_SPACING = 25
SPACING_PATTERN = [20, 30, 45, 65, 45, 30, 20]
PATTERN_LEN = len(SPACING_PATTERN)

# Layer Names (only Plan and Elevation)
LAYERS = ["Plan", "Elevation"]

def add_layers(doc):
    for name in LAYERS:
        if name not in doc.layers:
            doc.layers.new(name)

def draw_rectangle(msp, layer, x, y, width, height):
    msp.add_lwpolyline(
        [(x, y), (x + width, y), (x + width, y + height),
         (x, y + height), (x, y)],
        dxfattribs={"layer": layer}
    )

def main(filename):
    # Create DXF with R2018 version
    doc = ezdxf.new(setup=True, dxfversion="R2018")
    msp = doc.modelspace()
    add_layers(doc)

    # === Plan View ===
    gap = (X_TOTAL - 3 * PHL) / 2
    horiz_positions = [0, PHL + gap, 2 * (PHL + gap)]

    for x in horiz_positions:
        y = 0
        draw_rectangle(msp, "Plan", x, y, PHL, PHW)  # Bottom row
        draw_rectangle(msp, "Plan", x, y + Z_OFFSET, PHL, PHW)  # Top row

    x = EDGE_SPACING
    spacing_index = 0
    vertical_pipe_positions = []
    while x + PVW <= X_TOTAL:
        y = -PVW
        draw_rectangle(msp, "Plan", x, y, PVW, PVW)
        vertical_pipe_positions.append(x)
        x += PVH + SPACING_PATTERN[spacing_index % PATTERN_LEN]
        spacing_index += 1

    # === Elevation View ===
    y_offset = -3000
    for x in horiz_positions:
        draw_rectangle(msp, "Elevation", x, y_offset + Z_BASE, PHL, PHH)
        draw_rectangle(msp, "Elevation", x, y_offset + Z_BASE + Z_OFFSET, PHL, PHH)

    for x in vertical_pipe_positions:
        draw_rectangle(msp, "Elevation", x, y_offset + Z_BOTTOM, PVW, PVL)

    # Save to file
    doc.saveas(filename)
    print(f"DXF file saved: {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_gate_dxf.py output_filename.dxf")
        sys.exit(1)
    main(sys.argv[1])
