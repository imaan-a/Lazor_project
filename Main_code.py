class Block:
    def __init__(self, position, type):
        self.position = position
        self.type = type

    def findedges(self):
        pass


class Grid:
    def __init__(self, position):
        self.position = position

    def findtype(self):
        pass

    def blockagestatus(self, direction_in):
        pass

# Main code starts here


def solve_bff(filename):
    initial_map, available_dict, required_intersection, initial_laser = read_bff(
        filename)

    while check_intersection(current_lazer_path, required_intersection):
        current_map = generate_arrangement(initial_map, available_dict)
        current_lazer_path = generate_lazer(current_map, initial_laser)

    generate_png(filename, current_map, current_lazer_path)
