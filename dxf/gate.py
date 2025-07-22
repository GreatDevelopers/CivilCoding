import ezdxf
import sys
from ezdxf.math import Vec2

# === Constants for geometry ===
INCH = 25.4  # Conversion factor to mm
PHL = 59.5 * INCH     # Pipe horizontal length
PHW = 1.5 * INCH      # Pipe horizontal width
PHH = 3 * INCH        # Pipe horizontal height (elevation)
Z_BASE = 10 * INCH    # Elevation base height of pipe
Z_OFFSET = 50 * INCH  # Vertical spacing between top and bottom horizontal pipes
X_TOTAL = 180 * INCH  # Total gate width

# Vertical pipe dimensions
PVW = 20              # Vertical pipe width and height (square pipe)
PVH = 20
PVL = 71 * INCH       # Vertical pipe length (in elevation)
Z_BOTTOM = 1 * INCH   # Bottom offset of vertical pipes in elevation

# Pipe spacing parameters
EDGE_SPACING = 25                         # Left offset for first vertical pipe
SPACING_PATTERN = [20, 30, 45, 65, 45, 30, 20]  # Repeating spacing pattern
PATTERN_LEN = len(SPACING_PATTERN)

# DXF Layers
DRAW_LAYERS = ["Plan", "Elevation"]         # Drawing layers for geometry
DIM_LAYERS = ["DimPlan", "DimElevation"]    # Dimension layers for general dimensions
SPACING_LAYER = "DimSpacing"                # Dedicated layer for spacing dimensions
ALL_LAYERS = DRAW_LAYERS + DIM_LAYERS + [SPACING_LAYER]

# Assign colors to layers (ACI index 1–255, 0 = BYBLOCK)
LAYER_COLORS = {
    "Plan": 1,          # Red
    "Elevation": 3,     # Green
    "DimPlan": 5,       # Blue
    "DimElevation": 6,  # Magenta
    "DimSpacing": 2     # Yellow
}

# Dimension Style Name
DIM_STYLE_NAME = "GATE_DIM"

# Dimension Style Parameters
ARROW_SIZE = 5.0
TEXT_HEIGHT = 3.5
EXT_LINE_OFFSET = 1.5
DIM_LINE_EXTENSION = 1.0


# === Create drawing, dimension, and spacing layers with colors ===
def add_layers(doc):
    for name in ALL_LAYERS:
        if name not in doc.layers:
            layer = doc.layers.new(name)
            if name in LAYER_COLORS:
                layer.color = LAYER_COLORS[name]  # Assign unique color to each layer


# === Draw a rectangle in a given layer and position ===
def draw_rectangle(msp, layer, x, y, width, height):
    msp.add_lwpolyline(
        [(x, y), (x + width, y), (x + width, y + height),
         (x, y + height), (x, y)],
        dxfattribs={"layer": layer}
    )


# === Define and add custom dimension style ===
def create_dimstyle(doc):
    dimstyles = doc.dimstyles
    if not dimstyles.has_entry(DIM_STYLE_NAME):
        dimstyles.new(
            name=DIM_STYLE_NAME,
            dxfattribs={
                'dimtxsty': 'STANDARD',     # Use default text style
                'dimscale': 20.0,
                'dimtxt': TEXT_HEIGHT,
                'dimexo': EXT_LINE_OFFSET,
                'dimasz': ARROW_SIZE,
                'dimexe': DIM_LINE_EXTENSION,
            }
        )


# === Add dimensions in Plan and Elevation views ===
def add_dimensions(msp, vertical_pipe_positions, gap, horiz_positions):
    # Plan View: bottom dimensions
    y_offset = -100
    layer = "DimPlan"

    # Add total gate width dimension (bottom of drawing)
    msp.add_linear_dim(
        base=(0, y_offset - 60),
        p1=(0, 0),
        p2=(X_TOTAL, 0),
        dimstyle=DIM_STYLE_NAME,
        override={'dimtad': 1},  # Text above dimension line
        dxfattribs={'layer': layer}
    ).render()

    # Add dimension showing horizontal gap between pipe groups
    msp.add_linear_dim(
        base=(PHL, y_offset - 100),
        p1=(PHL, 0),
        p2=(PHL + gap, 0),
        dimstyle=DIM_STYLE_NAME,
        dxfattribs={'layer': layer}
    ).render()

    # Add spacing dimensions between first few vertical pipes
    # Use separate layer for spacing dimensions
    spacing_layer = SPACING_LAYER
    for i in range(min(len(SPACING_PATTERN), len(vertical_pipe_positions) - 1)):
        x1 = vertical_pipe_positions[i] + PVW  # Right edge of pipe i
        x2 = vertical_pipe_positions[i + 1]    # Left edge of next pipe
        msp.add_linear_dim(
            base=(0, y_offset),
            p1=(x1, 0),
            p2=(x2, 0),
            dimstyle=DIM_STYLE_NAME,
            dxfattribs={'layer': spacing_layer}
        ).render()

    # Elevation View: vertical dimensions
    y_offset = -3000
    elev_layer = "DimElevation"

    # Add full height of vertical pipe
    msp.add_linear_dim(
        base=(-150, y_offset),
        p1=(0, y_offset + Z_BOTTOM),
        p2=(0, y_offset + Z_BOTTOM + PVL),
        angle=90,
        dimstyle=DIM_STYLE_NAME,
        dxfattribs={'layer': elev_layer}
    ).render()

    # Add vertical spacing between bottom and top horizontal pipe
    msp.add_linear_dim(
        base=(-100, y_offset + Z_BASE),
        p1=(0, y_offset + Z_BASE),
        p2=(0, y_offset + Z_BASE + Z_OFFSET),
        angle=90,
        dimstyle=DIM_STYLE_NAME,
        dxfattribs={'layer': elev_layer}
    ).render()


# === Main logic: draw geometry and add dimensions ===
def main(filename):
    doc = ezdxf.new(setup=True, dxfversion="R2018")
    msp = doc.modelspace()
    add_layers(doc)
    create_dimstyle(doc)

    # --- Plan View Geometry ---
    gap = (X_TOTAL - 3 * PHL) / 2  # Gap between horizontal pipe groups
    horiz_positions = [0, PHL + gap, 2 * (PHL + gap)]  # X positions for pipe groups

    # Draw bottom and top rows of horizontal pipes
    for x in horiz_positions:
        y = 0
        draw_rectangle(msp, "Plan", x, y, PHL, PHW)                 # Bottom row
        draw_rectangle(msp, "Plan", x, y + Z_OFFSET, PHL, PHW)      # Top row

    # Draw vertical pipes and collect their X positions
    x = EDGE_SPACING
    spacing_index = 0
    vertical_pipe_positions = []
    while x + PVW <= X_TOTAL:
        y = -PVW  # To ensure clear visibility in plan
        draw_rectangle(msp, "Plan", x, y, PVW, PVW)
        vertical_pipe_positions.append(x)
        x += PVH + SPACING_PATTERN[spacing_index % PATTERN_LEN]
        spacing_index += 1

    # --- Elevation View Geometry ---
    y_offset = -3000  # Shift down to separate from plan view
    for x in horiz_positions:
        draw_rectangle(msp, "Elevation", x, y_offset + Z_BASE, PHL, PHH)               # Bottom pipe
        draw_rectangle(msp, "Elevation", x, y_offset + Z_BASE + Z_OFFSET, PHL, PHH)    # Top pipe

    # Draw vertical pipes in elevation
    for x in vertical_pipe_positions:
        draw_rectangle(msp, "Elevation", x, y_offset + Z_BOTTOM, PVW, PVL)

    # --- Add dimensions ---
    add_dimensions(msp, vertical_pipe_positions, gap, horiz_positions)

    # --- Save DXF file ---
    doc.saveas(filename)
    print(f"DXF file saved: {filename}")


# === Run script with output filename ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_gate_dxf_with_dims.py output_filename.dxf")
        sys.exit(1)
    main(sys.argv[1])
