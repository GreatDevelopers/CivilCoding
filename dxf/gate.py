import ezdxf
import sys
import locale

# Ensure decimal separator is period (.)
locale.setlocale(locale.LC_NUMERIC, 'C')

INCH = 25.4

PHL = [59.625 * INCH, 57 * INCH, 57 * INCH]
gap = [2 / 8 * INCH, 1 / 8 * INCH]
X_TOTAL = sum(PHL) + sum(gap)
print(f"Total gate width (X_TOTAL): {X_TOTAL:.3f} mm")

PHW = 40
PHH = 80

PVW = 20
PVH = 20
TopLevel = 6 * 12 * INCH
Z_BOTTOM = 3 * INCH
PVL = TopLevel - Z_BOTTOM

Z_BASE = Z_BOTTOM
Z_OFFSET = TopLevel - 9 * INCH - PHH

EDGE_SPACING = 20
SPACING_PATTERN = [20, 32.5, 45, 65, 45, 32.5, 20]
PATTERN_LEN = len(SPACING_PATTERN)

VSPACE = 300
Y_PLAN_TOP = 0
Y_PLAN_BOT = Y_PLAN_TOP - 200 - VSPACE
Y_ELEV = Y_PLAN_BOT - 2200 - VSPACE

LAYER_DEFS = {
    "PlanTop": 1,
    "PlanBot": 3,
    "Elevation": 2,
    "DimPlanTP": 5,
    "DimPlanSpacing": 4,
    "DimPlanBP": 6,
    "DimElevation": 7
}

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
        "dimexo": 1,
        "dimasz": 5.0,
        "dimexe": 0.5
    },
}

def setup_layers(doc):
    for name, color in LAYER_DEFS.items():
        if name not in doc.layers:
            layer = doc.layers.new(name)
            layer.color = color

def setup_dimstyles(doc):
    for name, attrs in DIM_STYLES.items():
        if name not in doc.dimstyles:
            doc.dimstyles.new(name=name, dxfattribs=attrs)

def draw_rectangle(msp, layer, x, y, width, height):
    pts = [
        (x, y),
        (x + width, y),
        (x + width, y + height),
        (x, y + height),
        (x, y)
    ]
    msp.add_lwpolyline(pts, dxfattribs={"layer": layer})

def add_linear_dim(msp, layer, dimstyle, p1, p2, base, angle=0, location=None):
    """
    Add a linear dimension. If 'location' is supplied, it puts text exactly there (use for custom placement).
    """
    dim = msp.add_linear_dim(
        base=base, p1=p1, p2=p2, angle=angle,
        dimstyle=dimstyle,
        dxfattribs={"layer": layer},
        location=location
    )
    dim.render()

def main(filename):
    doc = ezdxf.new(setup=True, dxfversion="R2018")
    msp = doc.modelspace()
    setup_layers(doc)
    setup_dimstyles(doc)

    # Calculate X panel positions
    panels_x = [0]
    for i in range(2):
        panels_x.append(panels_x[-1] + PHL[i] + gap[i])

    # --- PLAN TOP PIPE ---
    y = Y_PLAN_TOP
    for i in range(3):
        draw_rectangle(msp, "PlanTop", panels_x[i], y, PHL[i], PHW)

    DIM_GAP = 100

    # (2) --- Dimension Tiers: Gaps above, panel/total widths below ---
    # Tier 1 (gaps) ABOVE the horizontal pipe
    for i in range(2):
        x1 = panels_x[i] + PHL[i]
        x2 = panels_x[i + 1]
        mid = (x1 + x2) / 2
        add_linear_dim(
            msp, "DimPlanTP", DIM_STYLE_MAIN,
            p1=(x1, y + PHW),
            p2=(x2, y + PHW),
            base=(mid, y + PHW + DIM_GAP),
            angle=0
        )

    # Tier 2 (panel widths) BELOW the horizontal pipe
    for i in range(3):
        x1 = panels_x[i]
        x2 = x1 + PHL[i]
        mid = (x1 + x2) / 2
        add_linear_dim(
            msp, "DimPlanTP", DIM_STYLE_MAIN,
            p1=(x1, y),
            p2=(x2, y),
            base=(mid, y - PHW - DIM_GAP),
            angle=0
        )

    # Tier 3 (overall width) FARTHER BELOW the pipe
    add_linear_dim(
        msp, "DimPlanTP", DIM_STYLE_MAIN,
        p1=(0, y),
        p2=(X_TOTAL, y),
        base=(X_TOTAL / 2, y - PHW - 2 * DIM_GAP),
        angle=0
    )

    # (1) --- Vertical dimension to THE LEFT of the start of the pipe ---
    # Instead of right of end, set at left of start (panels_x[0])
    add_linear_dim(
        msp, "DimPlanTP", DIM_STYLE_MAIN,
        p1=(panels_x[0], y),
        p2=(panels_x[0], y + PHW),
        base=(panels_x[0] - 50, y + PHW / 2),
        angle=90
    )

    # --- PLAN BOTTOM PIPE ---
    y = Y_PLAN_BOT
    for i in range(3):
        draw_rectangle(msp, "PlanBot", panels_x[i], y, PHL[i], PHW)

    x = EDGE_SPACING
    vertical_pipe_x = []
    i_pat = 0
    while x + PVW <= X_TOTAL:
        draw_rectangle(msp, "PlanBot", x, y - PVW, PVW, PVW)
        vertical_pipe_x.append(x)
        x += PVH + SPACING_PATTERN[i_pat % PATTERN_LEN]
        i_pat += 1

    pat_base_y = y - PHW - 5
    for i in range(1, len(vertical_pipe_x)):
        x1 = vertical_pipe_x[i - 1] + PVW
        x2 = vertical_pipe_x[i]
        mid = (x1 + x2) / 2
        add_linear_dim(
            msp, "DimPlanSpacing", DIM_STYLE_BOTTOM,
            p1=(x1, y),
            p2=(x2, y),
            base=(mid, pat_base_y),
            angle=0
        )

    # (3) --- Square pipe (20x20mm) size, show both H and V dimensions next to one square pipe (not at far end) ---
    # Pick the first vertical pipe for clarity
    sq_x = vertical_pipe_x[0]
    sq_y = y - PVW

    # Horizontal
    add_linear_dim(
        msp, "DimPlanBP", DIM_STYLE_BOTTOM,
        p1=(sq_x, sq_y),
        p2=(sq_x + PVW, sq_y),
        base=(sq_x + PVW / 2, sq_y - 25),  # Below the square
        angle=0
    )
    # Vertical
    add_linear_dim(
        msp, "DimPlanBP", DIM_STYLE_BOTTOM,
        p1=(sq_x, sq_y),
        p2=(sq_x, sq_y + PVW),
        base=(sq_x - 25, sq_y + PVW / 2),  # Left of the square
        angle=90
    )

    # Dimension bar size (rectangle, right of plan)
    right_x = X_TOTAL
    add_linear_dim(
        msp, "DimPlanBP", DIM_STYLE_BOTTOM,
        p1=(right_x, y), p2=(right_x, y + PHW),
        base=(right_x + 10, y + PHW / 2),
        angle=90
    )

    # --- ELEVATION ---
    y = Y_ELEV
    for i in range(3):
        draw_rectangle(msp, "Elevation", panels_x[i], y + Z_BASE, PHL[i], PHH)
        draw_rectangle(msp, "Elevation", panels_x[i], y + Z_BASE + Z_OFFSET, PHL[i], PHH)
    for xp in vertical_pipe_x:
        draw_rectangle(msp, "Elevation", xp, y + Z_BOTTOM, PVW, PVL)

    elev_y_max = y + Z_BASE + PHH + Z_OFFSET + 80
    add_linear_dim(
        msp, "DimElevation", DIM_STYLE_MAIN,
        p1=(0, elev_y_max), p2=(X_TOTAL, elev_y_max),
        base=(X_TOTAL / 2, elev_y_max + 30 + 120),
        angle=0
    )

    add_linear_dim(
        msp, "DimElevation", DIM_STYLE_MAIN,
        p1=(X_TOTAL + 80, y + Z_BOTTOM), p2=(X_TOTAL + 80, y + Z_BOTTOM + PVL),
        base=(X_TOTAL + 110, y + Z_BOTTOM + PVL / 2),
        angle=90
    )

    pipe0x = vertical_pipe_x[0]
    add_linear_dim(
        msp, "DimElevation", DIM_STYLE_MAIN,
        p1=(pipe0x, y), p2=(pipe0x, y + Z_BOTTOM),
        base=(pipe0x - 40, y + Z_BOTTOM / 2),
        angle=90
    )

    doc.saveas(filename)
    print(f"DXF file saved: {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_gate_dxf.py output_filename.dxf")
        sys.exit(1)
    main(sys.argv[1])
