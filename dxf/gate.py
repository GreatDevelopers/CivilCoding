import ezdxf
from ezdxf.math import Vec2
import sys

# Constants
INCH = 25.4  # mm
PHL = 59.5 * INCH     # Horizontal pipe length
PHW = 1.5 * INCH      # Horizontal pipe width
PHH = 3 * INCH        # Horizontal pipe height
Z_BASE = 10 * INCH    # Bottom row height
Z_OFFSET = 50 * INCH  # Vertical distance between two rows
X_TOTAL = 180 * INCH  # Total width of gate
PVW = 20              # Vertical pipe width (and depth)
PVH = 20              # Vertical pipe depth
PVL = 71 * INCH       # Vertical pipe height
Z_BOTTOM = 1 * INCH   # Vertical pipe bottom
EDGE_SPACING = 25     # X offset of first vertical pipe
SPACING_PATTERN = [20, 30, 45, 65, 45, 30, 20]
PATTERN_LEN = len(SPACING_PATTERN)
SCALE = 1  # for arrows/text size etc.

# Layer Names
LAYERS = ["Plan", "PlanDimensions", "Elevation", "ElevationDimensions"]

def add_layers(doc):
    for name in LAYERS:
        if name not in doc.layers:
            doc.layers.new(name)

def draw_rectangle(msp, layer, x, y, width, height):
    msp.add_lwpolyline(
        [(x, y), (x + width, y), (x + width, y + height), (x, y + height), (x, y)],
        dxfattribs={"layer": layer}
    )

def draw_dimension(msp, start, end, offset, text, layer):
    """
    Draws a linear dimension with a line, arrows and text label.
    start, end: Vec2 points
    offset: Vec2 direction for placing dimension line
    """
    # Draw dimension line
    dim_start = start + offset
    dim_end = end + offset
    msp.add_line(start, dim_start, dxfattribs={"layer": layer})
    msp.add_line(end, dim_end, dxfattribs={"layer": layer})
    msp.add_line(dim_start, dim_end, dxfattribs={"layer": layer})

    # Arrows
    arrow_size = 5 * SCALE
    for pt in [dim_start, dim_end]:
        msp.add_line(pt + Vec2(-arrow_size, -arrow_size),
                     pt, dxfattribs={"layer": layer})
        msp.add_line(pt + Vec2(-arrow_size, arrow_size),
                     pt, dxfattribs={"layer": layer})

    # Text
    mid = (dim_start + dim_end) / 2
    msp.add_text(
        text,
        dxfattribs={
            "height": 5 * SCALE,
            "layer": layer,
            "halign": 1,  # Center
            "valign": 2   # Middle
        }
    ).dxf.insert = mid

def main(filename):
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()
    add_layers(doc)

    # === Plan View ===
    gap = (X_TOTAL - 3 * PHL) / 2
    horiz_positions = [0, PHL + gap, 2 * (PHL + gap)]

    for x in horiz_positions:
        y = 0
        draw_rectangle(msp, "Plan", x, y, PHL, PHW)  # Bottom row
        draw_rectangle(msp, "Plan", x, y + Z_OFFSET, PHL, PHW)  # Top row

    # Vertical pipes (plan view = square)
    x = EDGE_SPACING
    spacing_index = 0
    vertical_pipe_positions = []
    while x + PVW <= X_TOTAL:
        y = -PVW
        draw_rectangle(msp, "Plan", x, y, PVW, PVW)
        vertical_pipe_positions.append(x)
        x += PVH + SPACING_PATTERN[spacing_index % PATTERN_LEN]
        spacing_index += 1

    # === Plan Dimensions ===
    # Overall length
    draw_dimension(msp, Vec2(0, -50), Vec2(X_TOTAL, -50),
                   Vec2(0, -20), f"{X_TOTAL:.1f} mm", "PlanDimensions")
    # Vertical pipe spacing (first two only)
    for i in range(min(2, len(vertical_pipe_positions) - 1)):
        x1 = vertical_pipe_positions[i]
        x2 = vertical_pipe_positions[i + 1]
        spacing = x2 - x1
        draw_dimension(msp, Vec2(x1, -10), Vec2(x2, -10),
                       Vec2(0, -20 - 15 * i), f"{spacing:.1f} mm", "PlanDimensions")
    # Pipe size
    draw_dimension(msp, Vec2(PHL / 2 - 100, Z_OFFSET + PHW + 10),
                   Vec2(PHL / 2 + 100, Z_OFFSET + PHW + 10),
                   Vec2(0, 10), f"{PHL:.1f}×{PHW:.1f} mm", "PlanDimensions")
    draw_dimension(msp, Vec2(vertical_pipe_positions[0], -PVW - 30),
                   Vec2(vertical_pipe_positions[0] + PVW, -PVW - 30),
                   Vec2(0, -10), f"{PVW}×{PVW} mm", "PlanDimensions")
    # Offset from origin
    draw_dimension(msp, Vec2(0, 0), Vec2(EDGE_SPACING, 0),
                   Vec2(0, -40), f"{EDGE_SPACING} mm offset", "PlanDimensions")

    # === Elevation View ===
    y_offset = -3000  # Drop elevation view below plan
    for x in horiz_positions:
        draw_rectangle(msp, "Elevation", x, y_offset + Z_BASE, PHL, PHH)  # Bottom row
        draw_rectangle(msp, "Elevation", x, y_offset + Z_BASE + Z_OFFSET, PHL, PHH)  # Top row

    # Vertical pipes (elevation = vertical rectangle)
    for x in vertical_pipe_positions:
        draw_rectangle(msp, "Elevation", x, y_offset + Z_BOTTOM, PVW, PVL)

    # === Elevation Dimensions ===
    # Overall height
    draw_dimension(msp,
                   Vec2(-50, y_offset + Z_BOTTOM),
                   Vec2(-50, y_offset + Z_BOTTOM + PVL),
                   Vec2(-20, 0),
                   f"{PVL:.1f} mm", "ElevationDimensions")
    # Horizontal pipe height
    draw_dimension(msp,
                   Vec2(horiz_positions[0], y_offset + Z_BASE),
                   Vec2(horiz_positions[0], y_offset + Z_BASE + Z_OFFSET),
                   Vec2(-30, 0),
                   f"{Z_OFFSET:.1f} mm", "ElevationDimensions")

    # Pipe thickness (only once)
    draw_dimension(msp,
                   Vec2(horiz_positions[0] + PHL + 30, y_offset + Z_BASE),
                   Vec2(horiz_positions[0] + PHL + 30, y_offset + Z_BASE + PHH),
                   Vec2(20, 0),
                   f"{PHH:.1f} mm", "ElevationDimensions")

    # Save to file
    doc.saveas(filename)
    print(f"DXF file saved: {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_gate_dxf.py output.dxf")
        sys.exit(1)
    main(sys.argv[1])
