import ezdxf
# No specific import for lineweight constants is needed if using direct integer values.

def create_dxf_with_layers_and_triangle():
    """
    Creates a DXF document with two layers, draws a triangle on Layer 1,
    and hatches it on Layer 2.
    """
    # Create a new DXF document
    # Using 'R2018' format for broader compatibility and setup=True for default settings
    doc = ezdxf.new('R2018', setup=True)
    msp = doc.modelspace()

    # Define Layer 1: Red color, line weight 5mm (as close as possible)
    # DXF lineweight units are 1/100th of a millimeter.
    # The value 500 (for 5mm) is outside the standard DXF lineweight range.
    # The maximum standard lineweight available in ezdxf is 211 (2.11mm).
    # Setting to 211 as the closest possible standard thick lineweight,
    # using the direct integer value as per VALID_DXF_LINEWEIGHTS.
    doc.layers.add(
        "Layer 1",
        color=ezdxf.colors.RED,
        lineweight=211  # Closest to 5mm (2.11mm), direct integer value
    )

    # Define Layer 2: Green color, line weight 0 (default/thin)
    # Using the direct integer value 0 for 0.00 mm lineweight.
    doc.layers.add(
        "Layer 2",
        color=ezdxf.colors.GREEN,
        lineweight=0  # 0.00 mm, default thin line, direct integer value
    )

    # Define triangle vertices
    # Base 60mm, Height 120mm
    # Vertices: (0,0), (6,0), (3,12)
    triangle_vertices = [
        (0, 0),
        (6, 0),
        (3, 12)
    ]

    # Draw the triangle on Layer 1
    # Using LWPOLYLINE for a closed polygon
    msp.add_lwpolyline(
        triangle_vertices,
        dxfattribs={
            'layer': "Layer 1",
            'closed': True  # Ensure the polyline is closed
        }
    )

    # Hatch the triangle on Layer 2
    # Create a Hatch entity
    hatch = msp.add_hatch(
        dxfattribs={
            'layer': "Layer 2",
            # 'pattern_fill_scale': 10 # Not needed for solid fill, but kept for reference
        }
    )

    # Add the boundary path for the hatch using hatch.paths.add_polyline_path
    # The path must be a closed loop
    hatch.paths.add_polyline_path(triangle_vertices, is_closed=True) # is_closed=True indicates a closed loop

    # Set the hatch pattern to SOLID fill
    hatch.set_solid_fill(color=ezdxf.colors.GREEN) # Use the layer's color for the solid fill

    # Save the DXF document
    file_name = "triangle_with_hatch.dxf"
    doc.saveas(file_name)
    print(f"DXF file '{file_name}' created successfully.")

if __name__ == "__main__":
    create_dxf_with_layers_and_triangle()
