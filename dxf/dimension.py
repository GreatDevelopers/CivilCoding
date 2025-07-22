import ezdxf
from ezdxf.math import Vec2

# Dimension Style Parameters
DIM_STYLE_NAME = "GATE_DIM"
ARROW_SIZE = 5.0       # Arrow size
TEXT_HEIGHT = 3.5      # Text height
EXT_LINE_OFFSET = 1.5  # Offset from measured point
DIM_LINE_EXTENSION = 1.0

# Gate Dimensions (in mm)
GATE_WIDTH = 3600
GATE_HEIGHT = 1500

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
        print(f"Created dimstyle '{DIM_STYLE_NAME}'")
    else:
        print(f"Dimstyle '{DIM_STYLE_NAME}' already exists")

def draw_gate_dxf(output_path):
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()

    # Create Dimension Style
    create_dimstyle(doc)

    # Draw gate frame rectangle
    gate_points = [(0, 0), (GATE_WIDTH, 0), (GATE_WIDTH, GATE_HEIGHT), (0, GATE_HEIGHT)]
    msp.add_lwpolyline(gate_points, close=True)

    # Horizontal dimension (bottom)
    msp.add_linear_dim(
        base=(0, -100),  # Y offset to place dim below
        p1=(0, 0),
        p2=(GATE_WIDTH, 0),
        dimstyle=DIM_STYLE_NAME
    ).render()

    # Vertical dimension (left)
    msp.add_linear_dim(
        base=(-150, 0),  # X offset to place dim left of gate
        p1=(0, 0),
        p2=(0, GATE_HEIGHT),
        angle=90,
        dimstyle=DIM_STYLE_NAME
    ).render()

    # Save the DXF
    doc.saveas(output_path)
    print(f"DXF saved at {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python generate_gate_dxf.py output.dxf")
    else:
        draw_gate_dxf(sys.argv[1])
