# BIM in FreeCAD

## Wall

The `Arch.makeWall()` function in FreeCAD's BIM/Arch workbench creates
parametric wall objects either from scratch or based on existing
geometry. Below is a detailed explanation of its parameters and usage:

### Function Syntax

```python
makeWall(baseobj=None, length=None, width=None, height=None, align="Center", face=None, name="GivenWallName")
```

### Parameters

1. `baseobj` (optional):
    - The foundation geometry for the wall. Accepts:
        - Linear 2D objects (lines, wires, sketches): Uses their
            path for wall direction. `width` defines thickness,
            `height` sets extrusion. `length` is ignored.
        - Faces: Only `height` is used; `length`/`width` ignored.
          Vertical faces use `width` for extrusion.
        - Solids/Meshes: Adopts the object's shape; all dimension
            parameter signored.
    - If `None`, creates a rectangular wall using `length`,
            `width`, and `height`.
2. `length`, `width`, `height` (optional):
    - Define dimensions when `baseobj=None`. Units follow FreeCAD's default (typically mm).
    - With a `baseobj`:
        - `width` = wall thickness (always used for linear bases).
        - `height` = extrusion length (used for all non-solid bases).
        - `length` is unused if a base object exists.
3. `align` (optional, default=`"Center"`):
    - Alignment relative to the `baseobj`'s path:
        - `"Left"`: Wall left of path.
        - `"Center"`: Wall centered on path.
        - `"Right"`: Wall right of path.
4. `face` (optional):
    - Index of a specific face on `baseobj` to extrude (if the object has multiple faces).
    - Example: `face=3` uses the fourth face of the base object.
5. `name` (optional):
    - Label for the generated wall object in the FreeCAD document.

### Usage Examples

#### 1. Wall from a Draft Line:

```python
import FreeCAD, Draft, Arch

# Create baseline
p1 = FreeCAD.Vector(0, 0, 0)
p2 = FreeCAD.Vector(2000, 0, 0)
baseline = Draft.makeLine(p1, p2)

# Build wall (width=150mm, height=4000mm)
GivenWallName1 = Arch.makeWall(baseline, width=230, height=3500)
FreeCAD.ActiveDocument.recompute()
```

- Result: Wall follows the line; `width`/`height` set dimensions.


#### 2. Wall from Scratch:

```python
# Create standalone wall (length=2000mm, width=200mm, height=1000mm)
GivenWallName2 = Arch.makeWall(None, length=2000, width=200, height=1000)
Draft.move(GivenWallName2, FreeCAD.Vector(0, -1000, 0))  # Reposition
FreeCAD.ActiveDocument.recompute()
```

- Result: Rectangular wall with specified dimensions.


#### 3. Wall on a Specific Face:

```python
# Assuming 'obj' is a solid with multiple faces
GivenWallName3 = Arch.makeWall(obj, height=3000, face=2)  # Use third face
```
- Result: Wall extruded from face index 2.

## References

1. https://wiki.freecad.org/Arch_Wall/sv
1. https://yorikvanhavre.gitbooks.io/freecad-documentation/content/command-reference/Arch_Wall.html
1. https://freecad.github.io/SourceDoc/d2/d8e/namespaceArchWall.html
1. https://wiki.freecad.org/Arch_Wall
1. https://wiki.freecad.org/BIM_Workbench
1. https://forum.freecad.org/viewtopic.php?t=33133
1. https://wiki.freecad.org/Arch_MergeWalls/pt-br
1. https://wiki.freecad.org/Arch_Workbench
1. https://wiki.freecad.org/Arch_API
1. https://wiki.freecad.org/Arch_Check

