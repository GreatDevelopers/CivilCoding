# Door and Window: Readymade

The `Arch.makeWindowPreset()` function in FreeCAD creates parametric
window or door objects using predefined templates, simplifying the 
insertion of architectural elements into walls. Below is a detailed
breakdown of its parameters and usage:

### Function Syntax

```python
makeWindowPreset(preset_type, width, height, h1, h2, h3, w1, w2, o1, o2, placement=None)
```


### Parameters

1. `preset_type` (string):
    - Specifies the window/door template (e.g., `"Fixed"`,
      `"Glass door"`, `"Simple door"`, `"Opening only`). Refer Note 1
       below.
    - Defines the structural layout (frame divisions, panel types).
2. `width` and `height` (float):
    - Overall dimensions of the window/door in millimeters.
    - Example: `width=800.0`, `height=600.0`.
3. Frame Parameters (control subdivision dimensions):
    - `h1`, `h2`, `h3`: Horizontal dimensions (e.g., top/middle/bottom
      frame heights).
    - `w1`, `w2`: Vertical dimensions (e.g., left/right frame widths).
    - `o1`, `o2`: Offsets (e.g., panel inset from frame).
    - Example: `h1=3.0, h2=3.0, h3=3.0, w1=3.0, w2=3.0, o1=3.0, o2=3.0`.
4. `placement` (optional, `FreeCAD.Placement`):
    - Position and orientation in 3D space. If omitted, the window is
      placed at the origin.
    - Example: `placement=FreeCAD.Placement(FreeCAD.Vector(300,0,500),
      FreeCAD.Rotation())`.

### Usage Example

```python
import FreeCAD, Arch

# Define placement (position and rotation)
pl = FreeCAD.Placement(FreeCAD.Vector(300.0, 0.0, 500.0),
     FreeCAD.Rotation())

# Create a window using the "Open 1-pane" preset
Mywin01 = Arch.makeWindowPreset(
    'Open 1-pane', 
    width=800.0, 
    height=800.0, 
    h1=3.0, h2=3.0, h3=3.0, 
    w1=3.0, w2=3.0, 
    o1=3.0, o2=3.0, 
    placement=pl
)

# Attach to a host wall (optional)
Mywin01.Hosts = [FreeCAD.ActiveDocument.GivenWallName]
FreeCAD.ActiveDocument.recompute()
```


### Key Notes

- Dynamic Adjustments: After creation, modify `width`/`height` directly
  via the object's properties. Frame parameters (e.g., `h1`, `w1`)
  require editing the underlying sketch.
- Host Attachment: Assign a wall to `Hosts` to subtract the window
  volume automatically.
- Preset Variants: Includes doors, fixed windows, and multi-pane
  designs (e.g., 2-pane sliding windows).
- Customisation: For non-standard designs, create a sketch manually and
  use `Arch.makeWindow()`.


### Advanced Workflow

- Opening Animation: Set `Opening` property (0–100%) to visualise open
  states.
- Component Extraction: Use macros to separate frames/panes for
  rendering:

```python
import Part
for solid in Mywin01.Shape.Solids:
    Part.show(solid)
```

Note:

1. At the time of writing this, list of preset  is:
    1. Awning
    2. Fixed
    3. Glass door
    4. Open 1-pane
    5. Open 2-pane
    6. Opening only
    7. Sash 2-pane
    8. Simple door
    9. Sliding 2-pane
    10. Sliding 4-pane

## References

1. https://github.com/FreeCAD/FreeCAD/issues/14751
1. https://forum.freecad.org/viewtopic.php?t=44965\&start=160
1. https://forum.freecad.org/viewtopic.php?style=3\&t=4741
1. https://freecad.github.io/SourceDoc/d3/db7/namespaceArchWindow.html
1. https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Tutorial_for_open_windows.md
1. https://wiki.freecad.org/Arch_Window
1. https://forum.freecad.org/viewtopic.php?t=26419
1. https://www.freecad.org/manual/a-freecad-manual.pdf
1. https://wiki.freecad.org/Arch_tutorial
1. https://wiki.archlinux.org/title/Kernel_parameters
1. https://wiki.archlinux.org/title/Window_manager
1. https://www.reddit.com/r/archlinux/comments/q7z0fj/what_kernel_parameters_do_you_use/
1. https://www.reddit.com/r/archlinux/comments/thmfd8/factory_reset_arch/
1. https://bbs.archlinux.org/viewtopic.php?id=131342
1. https://wiki.archlinux.org/title/Dual_boot_with_Windows
1. https://www.youtube.com/watch?v=8mxB6-2Ec3U
1. https://support.graphisoft.com/hc/en-us/articles/34225668998545-How-to-create-a-window-with-a-masonry-arch
1. https://www.mathworks.com/help/systemcomposer/ref/systemcomposer.arch.parameter.html
1. https://wiki.archlinux.org/title/Power_management/Suspend_and_hibernate
1. https://www.youtube.com/watch?v=2SnjJEuaMH8
1. https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/windows-setup-automation-overview?view=windows-11
1. https://stackoverflow.com/questions/16568901/what-exactly-does-the-arch-argument-on-the-candle-command-line-do
1. https://www.debugpoint.com/archinstall-guide/
1. https://www.youtube.com/watch?v=2vbrFZiq2Hc
1. https://www.youtube.com/watch?v=LSXAgxc714E
1. https://www.youtube.com/watch?v=ZJ8sYIR3zrU
1. https://www.youtube.com/watch?v=fzbVuTW7GyU
1. https://github.com/FreeCAD/FreeCAD/blob/main/src/Mod/BIM/ArchWindowPresets.py#L31

