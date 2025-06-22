import json
import math

INPUT_FILE = "building.txt"
OUTPUT_FILE = "parseddata.json"

def parse_defaults(lines):
    defaults = {}
    for line in lines:
        if '=' in line:
            key, val = map(str.strip, line.split('=', 1))
            if key == "brick_colour":
                color_map = {}
                for pair in val.split():
                    k, v = pair.split(":")
                    color_map[k] = v
                defaults[key] = color_map
            elif key in ("brick", "wall_height", "wall_thickness", "lintel_level", "sill_level"):
                try:
                    defaults[key] = float(val)
                except ValueError:
                    defaults[key] = val
            else:
                defaults[key] = val
    return defaults

def parse_types(lines, defaults, is_window=False):
    result = {}
    sill = defaults.get("sill_level", 1000.0)
    lintel = defaults.get("lintel_level", 2100.0)

    for line in lines:
        if '=' not in line:
            continue
        key, val = map(str.strip, line.split('=', 1))
        parts = [v.strip() for v in val.split(',')]

        if len(parts) == 2:
            preset, width_str = parts
            height = lintel - sill if is_window else lintel
        elif len(parts) == 3:
            preset, width_str, height_str = parts
            height = float(height_str) if height_str else (lintel - sill if is_window else lintel)
        else:
            continue

        try:
            width = float(width_str)
        except ValueError:
            continue

        result[key] = {
            "preset": preset,
            "width": round(width, 4),
            "height": round(height, 4)
        }

    return result

def direction_to_angle(direction):
    return {
        "N": 90,
        "E": 0,
        "S": 270,
        "W": 180
    }.get(direction.upper())

def parse_wall_line(line, defaults):
    label, rest = map(str.strip, line.split(":", 1))
    tokens = rest.split()
    start = tokens.pop(0)
    x0, y0 = map(float, start.split(","))
    start_point = [x0, y0]
    curr_angle = None
    points = [start_point[:]]

    height = float(defaults.get("wall_height", 3000))
    thickness_factor = float(defaults.get("wall_thickness", 1.0))
    brick = float(defaults.get("brick", 230.0))
    thickness = round(thickness_factor * brick, 4)
    closed = False

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.lower() == 'c':
            closed = True
            i += 1
            continue
        if token.lower() == 'o':
            i += 1
            continue
        if '=' in token:
            key, val = token.split("=")
            if key == "height":
                height = float(val)
            elif key in ("thick", "thickness"):
                thickness = round(float(val) * brick, 4)
            i += 1
            continue

        if token[-1].upper() in "NSEW":
            length = float(token[:-1])
            angle = direction_to_angle(token[-1])
        elif "<" in token:
            parts = token.split("<")
            length = float(parts[0])
            delta_angle = float(parts[1])
            if curr_angle is None:
                raise ValueError("First segment must use absolute direction (e.g. 3000E)")
            angle = (curr_angle + delta_angle) % 360
        else:
            raise ValueError(f"Invalid segment format: {token}")

        curr_angle = angle
        radians = math.radians(angle)
        dx = length * math.cos(radians)
        dy = length * math.sin(radians)
        x0 += dx
        y0 += dy
        points.append([round(x0, 4), round(y0, 4)])
        i += 1

    if closed and points[-1] != start_point:
        points.append(start_point[:])  # explicitly close the wall path

    return {
        "label": label,
        "start": start_point,
        "path": points,
        "height": round(height, 4),
        "thickness": thickness,
        "closed": closed,
        "openings": []
    }

def parse_opening_line(line, wall_map):
    label, rest = map(str.strip, line.split(":", 1))
    tokens = rest.split()
    i = 0
    while i < len(tokens):
        segment_token = tokens[i]
        if not segment_token.endswith(":"):
            print(f"⚠️ Unexpected token in opening data: {segment_token}")
            i += 1
            continue
        segment_index = int(segment_token[:-1])
        i += 1
        while i + 1 < len(tokens) and not tokens[i].endswith(":"):
            pos = float(tokens[i])
            ref = tokens[i + 1]
            i += 2
            wall_map[label]["openings"].append({
                "segment_index": segment_index,
                "position": round(pos, 4),
                "type": "window" if ref.upper().startswith("W") else "door",
                "ref": ref
            })

def convert_building_txt_to_json(txt_file, json_file):
    with open(txt_file) as f:
        lines = [line.strip() for line in f if line.strip()]

    section = None
    sections = {
        "defaults": [],
        "doors": [],
        "windows": [],
        "walls": [],
        "openings": []
    }

    for line in lines:
        if line.startswith("#"):
            label = line[1:].strip().lower()
            if "default" in label:
                section = "defaults"
            elif "door_type" in label:
                section = "doors"
            elif "window_type" in label:
                section = "windows"
            elif "wall_data" in label:
                section = "walls"
            elif "opening_data" in label:
                section = "openings"
            else:
                section = None
        elif section:
            sections[section].append(line)

    defaults = parse_defaults(sections["defaults"])
    door_types = parse_types(sections["doors"], defaults, is_window=False)
    window_types = parse_types(sections["windows"], defaults, is_window=True)

    wall_map = {}
    walls = []
    for line in sections["walls"]:
        wall = parse_wall_line(line, defaults)
        wall_map[wall["label"]] = wall
        walls.append(wall)

    for line in sections["openings"]:
        parse_opening_line(line, wall_map)

    result = {
        "defaults": defaults,
        "door_types": door_types,
        "window_types": window_types,
        "walls": walls
    }

    with open(json_file, "w") as f:
        json.dump(result, f, indent=4)
    print(f"✅ Converted '{txt_file}' → '{json_file}' successfully.")

if __name__ == "__main__":
    convert_building_txt_to_json(INPUT_FILE, OUTPUT_FILE)
