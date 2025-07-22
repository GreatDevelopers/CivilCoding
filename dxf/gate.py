import ezdxf
import sys
from ezdxf.math import Vec2

# === Constants for geometry ===
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

DRAW_LAYERS = ["Plan", "Elevation"]
DIM_LAYERS = ["DimPlan", "DimElevation"]
SPACING_LAYER = "DimSpacing"
ALL_LAYERS = DRAW_LAYERS + DIM_LAYERS + [SPACING_LAYER]

LAYER_COLORS = {
    "Plan": 1,
    "Elevation": 3,
    "DimPlan": 5,
    "DimElevation": 6,
    "DimSpacing": 2
}

DIM_STYLE_NAME = "GATE_DIM"
ARROW_SIZE = 5.0
TEXT_HEIGHT = 3.5
EXT_LINE_OFFSET = 1.5
DIM_LINE_EXTENSION = 1.0

def add_layers(doc):
    for name in ALL_LAYERS:
        if name not in doc.layers:
            layer = doc.layers.new(name)
            if name in LAYER_COLORS:
                layer.color = LAYER_COLORS[name]

def draw_rectangle(msp, layer, x, y, width, height):
    msp.add_lwpolyline(
        [(x, y), (x + width, y), (x + width, y + height),
         (x, y + height), (x, y)],
        dxfattribs={"layer": layer}
    )

def create_dimstyle(doc):
    dimstyles = doc.dimstyles
    if not dimstyles.has_entry(DIM_STYLE_NAME):
        dimstyles.new(
            name=DIM_STYLE_NAME,
            dxfattribs={
                'dimtxsty': 'STANDARD',
                'dimscale': 20.0,
                'dimtxt': TEXT_HEIGHT,
                'dimexo': EXT_LINE_OFFSET,
                'dimasz': ARROW_SIZE,
                'dimexe': DIM_LINE_EXTENSION,
            }
        )

def add_dimensions(msp, vertical_pipe_positions, gap, horiz_positions):
    spacing_layer = SPACING_LAYER
    y_top = Z_OFFSET

    # --- Top row PLAN dimensions ---
    # 1st: Gap dimensions
    for i in range(len(horiz_positions) - 1):
        msp.add_linear_dim(
            base=(0, y_top - 20),
            p1=(horiz_positions[i] + PHL, y_top),
            p2=(horiz_positions[i+1], y_top),
            dimstyle=DIM_STYLE_NAME,
            dxfattribs={'layer': spacing_layer}
        ).render()

    # 2nd: Panel lengths
    for x in horiz_positions:
        msp.add_linear_dim(
            base=(0, y_top - 50),
            p1=(x, y_top),
            p2=(x + PHL, y_top),
            dimstyle=DIM_STYLE_NAME,
            dxfattribs={'layer': "DimPlan"}
        ).render()

    # 3rd: Total gate width
    msp.add_linear_dim(
        base=(0, y_top - 80),
        p1=(0, y_top),
        p2=(X_TOTAL, y_top),
        dimstyle=DIM_STYLE_NAME,
        dxfattribs={'layer': "DimPlan"}
    ).render()

    # --- Bottom row PLAN spacing and pipe size ---
    x1 = vertical_pipe_positions[0] + PVW
    x2 = vertical_pipe_positions[1]
    msp.add_linear_dim(
        base=(0, -50),
        p1=(x1, 0),
        p2=(x2, 0),
        dimstyle=DIM_STYLE_NAME,
        dxfattribs={'layer': spacing_layer}
    ).render()

    msp.add_linear_dim(
        base=(X_TOTAL + 30, 0),
        p1=(X_TOTAL + 30, 0),
        p2=(X_TOTAL + 30, PVW),
        angle=90,
        dimstyle=DIM_STYLE_NAME,
        dxfattribs={'layer': spacing_layer}
    ).render()

    # --- Elevation view dimensions ---
    elev_y_offset = -3000
    elev_layer = "DimElevation"

    # Offset from origin to bottom of vertical pipe
    msp.add_linear_dim(
        base=(-250, elev_y_offset + Z_BOTTOM),
        p1=(0, elev_y_offset),
        p2=(0, elev_y_offset + Z_BOTTOM),
        angle=90,
        dimstyle=DIM_STYLE_NAME,
        dxfattribs={'layer': elev_layer}
    ).render()

    # Full height of vertical pipe
    msp.add_linear_dim(
        base=(-400, elev_y_offset),
        p1=(0, elev_y_offset + Z_BOTTOM),
        p2=(0, elev_y_offset + Z_BOTTOM + PVL),
        angle=90,
        dimstyle=DIM_STYLE_NAME,
        dxfattribs={'layer': elev_layer}
    ).render()

    # Vertical spacing between pipes
    msp.add_linear_dim(
        base=(-300, elev_y_offset + Z_BASE),
        p1=(0, elev_y_offset + Z_BASE),
        p2=(0, elev_y_offset + Z_BASE + Z_OFFSET),
        angle=90,
        dimstyle=DIM_STYLE_NAME,
        dxfattribs={'layer': elev_layer}
    ).render()

def main(filename):
    doc = ezdxf.new(setup=True, dxfversion="R2018")
    msp = doc.modelspace()
    add_layers(doc)
    create_dimstyle(doc)

    gap = (X_TOTAL - 3 * PHL) / 2
    horiz_positions = [0, PHL + gap, 2 * (PHL + gap)]

    for x in horiz_positions:
        y = 0
        draw_rectangle(msp, "Plan", x, y, PHL, PHW)
        draw_rectangle(msp, "Plan", x, y + Z_OFFSET, PHL, PHW)

    x = EDGE_SPACING
    spacing_index = 0
    vertical_pipe_positions = []
    while x + PVW <= X_TOTAL:
        y = -PVW
        draw_rectangle(msp, "Plan", x, y, PVW, PVW)
        vertical_pipe_positions.append(x)
        x += PVH + SPACING_PATTERN[spacing_index % PATTERN_LEN]
        spacing_index += 1

    y_offset = -3000
    for x in horiz_positions:
        draw_rectangle(msp, "Elevation", x, y_offset + Z_BASE, PHL, PHH)
        draw_rectangle(msp, "Elevation", x, y_offset + Z_BASE + Z_OFFSET, PHL, PHH)

    for x in vertical_pipe_positions:
        draw_rectangle(msp, "Elevation", x, y_offset + Z_BOTTOM, PVW, PVL)

    add_dimensions(msp, vertical_pipe_positions, gap, horiz_positions)
    doc.saveas(filename)
    print(f"DXF file saved: {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_gate_dxf_with_dims.py output_filename.dxf")
        sys.exit(1)
    main(sys.argv[1])
