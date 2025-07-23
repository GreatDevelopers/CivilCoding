import ezdxf
import sys
import locale

# Ensure decimal separator is period (.) irrespective of system locale
locale.setlocale(locale.LC_NUMERIC, 'C')

# --- Constants (all dimensions in millimeters) ---
INCH = 25.4

# Panel lengths individually specified (3 panels)
PHL = [59.625 * INCH, 57 * INCH, 57 * INCH]

# Gaps between panels (two gaps)
gap = [2 / 8 * INCH, 1 / 8 * INCH]

# Calculate total gate width
X_TOTAL = sum(PHL) + sum(gap) # should be 14' 6"
print(f"Total gate width (X_TOTAL): {X_TOTAL:.3f} mm")

# Other geometry constants
PHW = 40 # * INCH  # Horizontal pipe width
PHH = 80    # Horizontal pipe height (elevation)

PVW = 20          # Pipe width for vertical pipes
PVH = 20          # Pipe height (same as width, square pipe)
TopLevel = 6*12*INCH
Z_BOTTOM = 3 * INCH
PVL = TopLevel - Z_BOTTOM   # Vertical pipe length (elevation)

Z_BASE = Z_BOTTOM # 10 * INCH
Z_OFFSET = TopLevel - 9 * INCH - PHH # 9" from top: 50 * INCH

EDGE_SPACING = 10
SPACING_PATTERN = [20, 30, 45, 65, 45, 30, 20]
PATTERN_LEN = len(SPACING_PATTERN)

# Layout vertical spacing to separate drawing zones
VSPACE = 300
Y_PLAN_TOP = 0
Y_PLAN_BOT = Y_PLAN_TOP - 200 - VSPACE
Y_ELEV = Y_PLAN_BOT - 2200 - VSPACE

# Layer names and colors (AutoCAD Color Index)
LAYER_DEFS = {
    "PlanTop": 1,         # Red
    "PlanBot": 3,         # Green
    "Elevation": 2,       # Yellow
    "DimPlanTP": 5,       # Blue
    "DimPlanSpacing": 4,  # Cyan
    "DimPlanBP": 6,       # Magenta
    "DimElevation": 7     # White
}

# Dimension style definitions with scales
DIM_STYLE_MAIN = "GATE_DIM"
DIM_STYLE_BOTTOM = "GATE_DIM_BOTTOM"
DIM_STYLES = {
    DIM_STYLE_MAIN: {
        "dimscale": 20.0,
        "dimtxsty": "STANDARD",
        "dimtxt": 3.5,
        "dimexo": 1.5,
        "dimasz": 5.0,
        "dimexe": 1.0
    },
    DIM_STYLE_BOTTOM: {
        "dimscale": 2.0,
        "dimtxsty": "STANDARD",
        "dimtxt": 3.5,
        "dimexo": 1, # 4.0,  # Larger offset for pipe spacing clarity
        "dimasz": 5.0,
        "dimexe": .5
    },
}

def setup_layers(doc):
    """Create layers with assigned colors."""
    for name, color in LAYER_DEFS.items():
        if name not in doc.layers:
            layer = doc.layers.new(name)
            layer.color = color

def setup_dimstyles(doc):
    """Create two dimension styles as needed."""
    for name, attrs in DIM_STYLES.items():
        if name not in doc.dimstyles:
            doc.dimstyles.new(name=name, dxfattribs=attrs)

def draw_rectangle(msp, layer, x, y, width, height):
    """Draw closed rectangle polyline on specified layer."""
    pts = [(x, y), (x + width, y), (x + width, y + height), (x, y + height), (x, y)]
    msp.add_lwpolyline(pts, dxfattribs={"layer": layer})

def add_linear_dim(msp, layer, dimstyle, p1, p2, base, angle=0):
    """
    Add linear dimension on selected layer and dimension style.
    All dimension components are automatically created on the appropriate layer.
    """
    msp.add_linear_dim(
        base=base, p1=p1, p2=p2, angle=angle,
        dimstyle=dimstyle,
        dxfattribs={"layer": layer}
    ).render()

def main(filename):
    doc = ezdxf.new(setup=True, dxfversion="R2018")
    msp = doc.modelspace()
    setup_layers(doc)
    setup_dimstyles(doc)

    # Calculate panel start X positions accounting for individual lengths and gaps
    panels_x = [0]
    for i in range(2):
        panels_x.append(panels_x[-1] + PHL[i] + gap[i])

    # --- PLAN TOP PIPE ---
    y = Y_PLAN_TOP
    for i in range(3):
        draw_rectangle(msp, "PlanTop", panels_x[i], y, PHL[i], PHW)

    DIM_GAP = 100  # Vertical gap between dimension tiers to avoid overlap

    # Tier 1: Gaps between panels
    for i in range(2):
        x1 = panels_x[i] + PHL[i]
        x2 = panels_x[i + 1]
        mid = (x1 + x2) / 2
        add_linear_dim(msp, "DimPlanTP", DIM_STYLE_MAIN,
                       p1=(x1, y), p2=(x2, y),
                       base=(mid, y - PHW - DIM_GAP),
                       angle=0)

    # Tier 2: Panel widths
    for i in range(3):
        x1 = panels_x[i]
        x2 = x1 + PHL[i]
        mid = (x1 + x2) / 2
        add_linear_dim(msp, "DimPlanTP", DIM_STYLE_MAIN,
                       p1=(x1, y), p2=(x2, y),
                       base=(mid, y - PHW - 2 * DIM_GAP),
                       angle=0)

    # Tier 3: Overall width (total gate width)
    add_linear_dim(msp, "DimPlanTP", DIM_STYLE_MAIN,
                   p1=(0, y), p2=(X_TOTAL, y),
                   base=(X_TOTAL / 2, y - PHW - 3 * DIM_GAP),
                   angle=0)

    # Vertical dimension to right of top pipe plan (pipe thickness)
    add_linear_dim(msp, "DimPlanTP", DIM_STYLE_MAIN,
                   p1=(X_TOTAL, y), p2=(X_TOTAL, y + PHW),
                   base=(X_TOTAL + 50, y + PHW / 2),
                   angle=90)

    # --- PLAN BOTTOM PIPE ---
    y = Y_PLAN_BOT
    for i in range(3):
        draw_rectangle(msp, "PlanBot", panels_x[i], y, PHL[i], PHW)

    # Draw vertical pipes and record pipe positions
    x = EDGE_SPACING
    vertical_pipe_x = []
    i_pat = 0
    while x + PVW <= X_TOTAL:
        draw_rectangle(msp, "PlanBot", x, y - PVW, PVW, PVW)
        vertical_pipe_x.append(x)
        x += PVH + SPACING_PATTERN[i_pat % PATTERN_LEN]
        i_pat += 1

    # Dimension all pipe spacings for entire gate width
    pat_base_y = y - PHW - 5 # reduced by ~30~
    for i in range(1, len(vertical_pipe_x)):
        x1 = vertical_pipe_x[i - 1] + PVW
        x2 = vertical_pipe_x[i]
        mid = (x1 + x2) / 2
        add_linear_dim(msp, "DimPlanSpacing", DIM_STYLE_BOTTOM,
                       p1=(x1, y), p2=(x2, y),
                       base=(mid, pat_base_y),
                       angle=0)

    # Dimension pipe size and rectangular pipe/bar size to right of bottom plan
    right_x = X_TOTAL + 30
    add_linear_dim(msp, "DimPlanBP", DIM_STYLE_BOTTOM,
                   p1=(right_x, y - PVW), p2=(right_x + PVW, y - PVW),
                   base=(right_x + PVW / 2, y - PVW - 20),
                   angle=0)
    add_linear_dim(msp, "DimPlanBP", DIM_STYLE_BOTTOM,
                   p1=(right_x + 40, y), p2=(right_x + 40, y + PHW),
                   base=(right_x + 60, y + PHW / 2),
                   angle=90)

    # --- ELEVATION ---
    y = Y_ELEV
    for i in range(3):
        draw_rectangle(msp, "Elevation", panels_x[i], y + Z_BASE, PHL[i], PHH)
        draw_rectangle(msp, "Elevation", panels_x[i], y + Z_BASE + Z_OFFSET, PHL[i], PHH)
    for xp in vertical_pipe_x:
        draw_rectangle(msp, "Elevation", xp, y + Z_BOTTOM, PVW, PVL)

    # Dimension overall width above elevation
    elev_y_max = y + Z_BASE + PHH + Z_OFFSET + 80
    add_linear_dim(msp, "DimElevation", DIM_STYLE_MAIN,
                   p1=(0, elev_y_max), p2=(X_TOTAL, elev_y_max),
                   base=(X_TOTAL / 2, elev_y_max + 30),
                   angle=0)

    # Dimension overall height to far right of elevation
    add_linear_dim(msp, "DimElevation", DIM_STYLE_MAIN,
                   p1=(X_TOTAL + 80, y + Z_BOTTOM), p2=(X_TOTAL + 80, y + Z_BOTTOM + PVL),
                   base=(X_TOTAL + 110, y + Z_BOTTOM + PVL / 2),
                   angle=90)

    # Dimension offset of first vertical pipe from ground (left bottom of elevation)
    pipe0x = vertical_pipe_x[0]
    add_linear_dim(msp, "DimElevation", DIM_STYLE_MAIN,
                   p1=(pipe0x, y), p2=(pipe0x, y + Z_BOTTOM),
                   base=(pipe0x - 40, y + Z_BOTTOM / 2),
                   angle=90)

    # Save DXF file
    doc.saveas(filename)
    print(f"DXF file saved: {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_gate_dxf.py output_filename.dxf")
        sys.exit(1)
    main(sys.argv[1])
