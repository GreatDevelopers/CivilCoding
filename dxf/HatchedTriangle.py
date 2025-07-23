import ezdxf

def create_dxf_with_layers_and_triangle():
    # Create a new DXF document with setup for default styles
    doc = ezdxf.new('R2018', setup=True)
    msp = doc.modelspace()

    # Add Layer 1: Red color, thick lineweight (~2.11 mm)
    doc.layers.add(
        name="Layer 1",
        color=ezdxf.colors.RED,
        lineweight=211  # Max supported lineweight (2.11 mm)
    )

    # Add Layer 2: Green color, default lineweight (0)
    doc.layers.add(
        name="Layer 2",
        color=ezdxf.colors.GREEN,
        lineweight=0
    )

    # Triangle vertices (base 60 mm, height 120 mm)
    triangle = [(0, 0), (6, 0), (3, 12)]

    # Draw triangle using closed polyline on Layer 1
    msp.add_lwpolyline(triangle, dxfattribs={
        'layer': "Layer 1",
        'closed': True
    })

    # Add solid hatch on Layer 2 using same triangle boundary
    hatch = msp.add_hatch(dxfattribs={'layer': "Layer 2"})
    hatch.paths.add_polyline_path(triangle, is_closed=True)
    hatch.set_solid_fill(color=ezdxf.colors.GREEN)

    # Save DXF file
    file_name = "triangle_with_hatch.dxf"
    doc.saveas(file_name)
    print(f"DXF file '{file_name}' created successfully.")

if __name__ == "__main__":
    create_dxf_with_layers_and_triangle()
