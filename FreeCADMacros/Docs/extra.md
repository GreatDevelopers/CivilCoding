### Notes

- Additions/Subtractions: Use `Arch.Add` and `Arch.Remove` to modify walls with other shapes.
- Automatic Height: Set `height=0` to inherit dimensions from parent objects (e.g., floors).
- Geometry Intersection: Place walls in a `Floor` object to handle intersections.
- Error Handling: Returns `None` if creation fails.

For advanced operations (e.g., joining walls), see `ArchWall.joinWalls()` in the
[SourceDoc](https://freecad.github.io/SourceDoc/d2/d8e/namespaceArchWall.html).
Related information may be found at [FreeCAD Wiki](https://wiki.freecad.org/Arch_Wall/sv).
