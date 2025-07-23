import ezdxf
import sys
import locale

# Ensure decimal separator uses a period
locale.setlocale(locale.LC_NUMERIC, 'C')

INCH = 25.4

PHL = [58.625 * INCH, 58.5 * INCH, 58.5 * INCH]
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

EDGE_SPACING = 38.95
SPACING_PATTERN = [20, 30, 45, 67.5, 45, 30, 20]
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

def draw_rectangle(msp, layer, x, y, width, height, color=None):
    pts = [
        (x, y),
        (x + width, y),
        (x + width, y + height),
        (x, y + height)
    ]
    msp.add_lwpolyline(pts + [pts[0]], dxfattribs={
        "layer": layer,
        "color": color if color is not None else 256
    })
    return pts

def hatch_rect(msp, layer, pts, color=256):
    hatch = msp.add_hatch(dxfattribs={'layer': layer})
    hatch.paths.add_polyline_path(pts + [pts[0]], is_closed=True)
    hatch.set_solid_fill(color=color)

def add_linear_dim(msp, layer, dimstyle, p1, p2, base, angle=0, location=None):
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

    panels_x = [0]
    for i in range(2):
        panels_x.append(panels_x[-1] + PHL[i] + gap[i])

    # --- PLAN TOP PIPE (80x40 mm, red and hatched red) ---
    y = Y_PLAN_TOP
    for i in range(3):
        pts = draw_rectangle(msp, "PlanTop", panels_x[i], y, PHL[i], PHW, color=1)
        hatch_rect(msp, "PlanTop", pts, color=1)

    DIM_GAP = 100

    # Tier dimensions (unchanged)
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
    add_linear_dim(
        msp, "DimPlanTP", DIM_STYLE_MAIN,
        p1=(0, y),
        p2=(X_TOTAL, y),
        base=(X_TOTAL / 2, y - PHW - 2 * DIM_GAP),
        angle=0
    )
    add_linear_dim(
        msp, "DimPlanTP", DIM_STYLE_MAIN,
        p1=(panels_x[0], y),
        p2=(panels_x[0], y + PHW),
        base=(panels_x[0] - 50, y + PHW / 2),
        angle=90
    )

    # --- PLAN BOTTOM PIPE (20x20 mm, green and hatched green) ---
    y = Y_PLAN_BOT
    for i in range(3):
        draw_rectangle(msp, "PlanBot", panels_x[i], y, PHL[i], PHW, color=1)
        hatch_rect(msp, "PlanBot", [
            (panels_x[i], y),
            (panels_x[i] + PHL[i], y),
            (panels_x[i] + PHL[i], y + PHW),
            (panels_x[i], y + PHW)
        ], color=1)

    x = EDGE_SPACING
    vertical_pipe_x = []
    i_pat = 0
    while x + PVW <= X_TOTAL:
        pts = [
            (x, y - PVW),
            (x + PVW, y - PVW),
            (x + PVW, y),
            (x, y)
        ]
        msp.add_lwpolyline(pts + [pts[0]], dxfattribs={"layer": "PlanBot", "color": 3})
        hatch_rect(msp, "PlanBot", pts, color=3)
        vertical_pipe_x.append(x)
        x += PVH + SPACING_PATTERN[i_pat % PATTERN_LEN]
        i_pat += 1

    pat_base_y = y - PHW - 5

    # --- Show spacing dimensions between vertical (square) pipes ---
    for i in range(1, len(vertical_pipe_x)):
        # Center-to-center spacing for visual clarity (alternatively use face-to-face)
        p1 = (vertical_pipe_x[i - 1] + PVW/2, y - PVW / 2)
        p2 = (vertical_pipe_x[i] + PVW/2, y - PVW / 2)
        base = ((p1[0] + p2[0]) / 2, pat_base_y - 20)
        add_linear_dim(
            msp, "DimPlanSpacing", DIM_STYLE_BOTTOM,
            p1=p1,
            p2=p2,
            base=base,
            angle=0
        )

    # Restore all previous edge and "span" dimensions (space from frame to first/last pipe and total)
    add_linear_dim(
        msp, "DimPlanSpacing", DIM_STYLE_BOTTOM,
        p1=(panels_x[0], y),
        p2=(vertical_pipe_x[0], y),
        base=((panels_x[0] + vertical_pipe_x[0]) / 2, y - PHW - 30),
        angle=0
    )
    last_panel_end = panels_x[2] + PHL[2]
    last_pipe_right = vertical_pipe_x[-1] + PVW
    add_linear_dim(
        msp, "DimPlanSpacing", DIM_STYLE_BOTTOM,
        p1=(last_pipe_right, y),
        p2=(last_panel_end, y),
        base=((last_pipe_right + last_panel_end) / 2, y - PHW - 30),
        angle=0
    )
    add_linear_dim(
        msp, "DimPlanSpacing", DIM_STYLE_BOTTOM,
        p1=(vertical_pipe_x[0], y),
        p2=(last_pipe_right, y),
        base=((vertical_pipe_x[0] + last_pipe_right) / 2, y - PHW - 60),
        angle=0
    )

    # Square pipe (20x20mm) hatch
    sq_x = vertical_pipe_x[0]
    sq_y = y - PVW
    sq_pts = [
        (sq_x, sq_y),
        (sq_x + PVW, sq_y),
        (sq_x + PVW, sq_y + PVW),
        (sq_x, sq_y + PVW)
    ]
    msp.add_lwpolyline(sq_pts + [sq_pts[0]], dxfattribs={"layer": "PlanBot", "color": 3})
    hatch_rect(msp, "PlanBot", sq_pts, color=3)

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
        # Horizontal 80x40 mm: base pipes, draw as red/hatch red
        pts = draw_rectangle(msp, "Elevation", panels_x[i], y + Z_BASE, PHL[i], PHH, color=1)
        hatch_rect(msp, "Elevation", pts, color=1)
        pts2 = draw_rectangle(msp, "Elevation", panels_x[i], y + Z_BASE + Z_OFFSET, PHL[i], PHH, color=1)
        hatch_rect(msp, "Elevation", pts2, color=1)

    for xp in vertical_pipe_x:
        elev_pts = [
            (xp, y + Z_BOTTOM),
            (xp + PVW, y + Z_BOTTOM),
            (xp + PVW, y + Z_BOTTOM + PVL),
            (xp, y + Z_BOTTOM + PVL)
        ]
        msp.add_lwpolyline(elev_pts + [elev_pts[0]], dxfattribs={"layer": "Elevation", "color": 3})
        hatch_rect(msp, "Elevation", elev_pts, color=3)

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
    elev_y_pipe = y + Z_BASE
    add_linear_dim(
        msp, "DimElevation", DIM_STYLE_MAIN,
        p1=(vertical_pipe_x[0], elev_y_pipe),
        p2=(vertical_pipe_x[-1] + PVW, elev_y_pipe),
        base=((vertical_pipe_x[0] + vertical_pipe_x[-1] + PVW) / 2, elev_y_pipe - PHH - 30),
        angle=0
    )
    pipe0x = vertical_pipe_x[0]
    add_linear_dim(
        msp, "DimElevation", DIM_STYLE_MAIN,
        p1=(pipe0x, y),
        p2=(pipe0x, y + Z_BOTTOM),
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
