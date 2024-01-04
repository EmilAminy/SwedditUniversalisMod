import re

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rotation:
    def __init__(self, value):
        self.value = value

class Height:
    def __init__(self, value):
        self.value = value

class Positions:
    def __init__(self, city, unit, text, port, route, battle, wind):
        self.city = city
        self.unit = unit
        self.text = text
        self.port = port
        self.route = route
        self.battle = battle
        self.wind = wind

class Heights:
    def __init__(self, city, unit, text, port, route, battle, wind):
        self.city = city
        self.unit = unit
        self.text = text
        self.port = port
        self.route = route
        self.battle = battle
        self.wind = wind

class Rotations:
    def __init__(self, city, unit, text, port, route, battle, wind):
        self.city = city
        self.unit = unit
        self.text = text
        self.port = port
        self.route = route
        self.battle = battle
        self.wind = wind

class ProvinceData:
    def __init__(self, name, id, positions, rotations, heights):
        self.name = name
        self.id = id
        self.positions = positions
        self.rotations = rotations
        self.heights = heights

def generate_positions(line):
    # Split the stripped line into a list of values
    values = line.split()

    # Check if there are 14 values (two coordinates for each of the seven elements)
    if len(values) != 14:
        raise ValueError("Invalid number of values for positions.")

    # Create Coordinate objects for each element
    city = Coordinate(float(values[0]), float(values[1]))
    unit = Coordinate(float(values[2]), float(values[3]))
    text = Coordinate(float(values[4]), float(values[5]))
    port = Coordinate(float(values[6]), float(values[7]))
    route = Coordinate(float(values[8]), float(values[9]))
    battle = Coordinate(float(values[10]), float(values[11]))
    wind = Coordinate(float(values[12]), float(values[13]))

    # Organize the coordinates into a Positions object
    positions = Positions(city, unit, text, port, route, battle, wind)

    return positions

def generate_rotations(line):
    # Split the stripped line into a list of rotation values
    values = line.split()

    # Check if there are 7 rotation values for the seven elements
    if len(values) != 7:
        raise ValueError("Invalid number of values for rotations.")

    # Create Rotation objects for each element
    city = Rotation(float(values[0]))
    unit = Rotation(float(values[1]))
    text = Rotation(float(values[2]))
    port = Rotation(float(values[3]))
    route = Rotation(float(values[4]))
    battle = Rotation(float(values[5]))
    wind = Rotation(float(values[6]))

    # Organize the rotations into a Rotations object
    rotations = Rotations(city, unit, text, port, route, battle, wind)

    return rotations

def generate_heights(line):
    # Split the stripped line into a list of height values
    values = line.split()

    # Check if there are 7 height values for the seven elements
    if len(values) != 7:
        raise ValueError("Invalid number of values for heights.")

    # Create Height objects for each element
    city = Height(float(values[0]))
    unit = Height(float(values[1]))
    text = Height(float(values[2]))
    port = Height(float(values[3]))
    route = Height(float(values[4]))
    battle = Height(float(values[5]))
    wind = Height(float(values[6]))

    # Organize the heights into a Heights object
    heights = Heights(city, unit, text, port, route, battle, wind)

    return heights


def generate_province_list(file):
    province_list = []
    current_province = None
    status = ''

    for line in file:
        line = line.lstrip()

        # if a new province is found
        if line.startswith('#'):
            if current_province:
                province_list.append(current_province)
            current_province = ProvinceData(line[1:], None, None, None, None)
            status = 'SEARCHING_ID'
            continue
        
        pattern = re.match(r'^\s*(\d+)={$', line)

        # if line contains the id
        if status == 'SEARCHING_ID' and pattern:
            current_province.id = pattern.group(1)
            status = 'SEARCHING_POSITIONS'
            continue

        # if line contains the positions indicator
        if status == 'SEARCHING_POSITIONS' and 'position' in line:
            status = 'HANDLING_POSITIONS'
            continue

        # the actual positions
        if status == 'HANDLING_POSITIONS':
            current_province.positions = generate_positions(line)
            status = 'SEARCHING_ROTATIONS'
            continue
        
        # if line contains the rotations indicator
        if status == 'SEARCHING_ROTATIONS' and 'rotation' in line:
            status = 'HANDLING_ROTATIONS'
            continue

        # the actual rotations
        if status == 'HANDLING_ROTATIONS':
            current_province.rotations = generate_rotations(line)
            status = 'SEARCHING_HEIGHTS'
            continue

        # if line contains the heights indicator
        if status == 'SEARCHING_HEIGHTS' and 'height' in line:
            status = 'HANDLING_HEIGHTS'
            continue

        # the actual heights
        if status == 'HANDLING_HEIGHTS':
            current_province.heights = generate_heights(line)
            status = ''
            continue
    
    province_list.append(current_province)
    return province_list

def provinces_to_file(province_list, output_filename):
    with open(output_filename, 'w') as output_file:
        for province in province_list:
            output_file.write(f"#{province.name}")
            output_file.write(f"{province.id}={{\n")
            
            # Write positions
            output_file.write("    position={\n")
            output_file.write("        ")
            for coordinate_name in ["city", "unit", "text", "port", "route", "battle", "wind"]:
                coordinate = getattr(province.positions, coordinate_name)
                output_file.write(f"{coordinate.x:.3f} {coordinate.y:.3f} ")
            output_file.write("\n    }\n")
            
            # Write rotations
            output_file.write("    rotation={\n")
            output_file.write("        ")
            for rotation_name in ["city", "unit", "text", "port", "route", "battle", "wind"]:
                rotation = getattr(province.rotations, rotation_name)
                output_file.write(f"{rotation.value:.3f} ")
            output_file.write("\n    }\n")
            
            # Write heights
            output_file.write("    height={\n")
            output_file.write("        ")
            for height_name in ["city", "unit", "text", "port", "route", "battle", "wind"]:
                height = getattr(province.heights, height_name)
                output_file.write(f"{height.value:.3f} ")
            output_file.write("\n    }\n")
            
            output_file.write("}\n")

def offset_position(province, offset_x, offset_y):
    for coordinate_name in ["city", "unit", "text", "port", "route", "battle", "wind"]:
        coordinate = getattr(province.positions, coordinate_name)
        coordinate.x += offset_x
        coordinate.y += offset_y
    return province


def offset_positions(province_list, offset_x, offset_y):
    for province in province_list:
        offset_position(province, offset_x, offset_y)
    return province_list

def remove_negative_waters(province_list):
    result = []
    for province in province_list:
        if (province.positions.wind.x != 0.000 or province.positions.wind.y != 0.000) and province.positions.city.x < 0:
            continue
        result.append(province)
    return result

def main():
    configure = True
    if configure:
        file = open('../positions.txt', 'r')
        provinces_to_file(province_list, '../positions.txt')
    else:
        file = open('positions.txt', 'r')
        province_list = generate_province_list(file)
        province_list = offset_positions(province_list, -2304, 0)
        province_list = remove_negative_waters(province_list)
        provinces_to_file(province_list, '../positions.txt')

# Running the program
if __name__ == "__main__":
    main()