from read_and_export import read_bff, generate_png
from map import generate_next_map
from laser import check_intersection, generate_laser


class Block:
    def __init__(self, position, type):
        self.position = position
        self.type = type

    def findedges(self):
        return [(self.position[0] + i[0], self.position[1] + i[1]) for i in [(0, -1), (0, 1), (-1, 0), (1, 0)]]

    def __eq__(self, other):
        if self.position == other.position and self.type == other.type:
            return True
        else:
            return False


class Grid:
    def __init__(self, position):
        self.position = position

    def findtype(self):
        if self.position[1] % 2 == 0:
            return 'horizontal'
        else:
            return 'vertical'

    def __eq__(self, other):
        if self.position == other.position:
            return True
        else:
            return False


# Main code starts here

def solve_bff(filename):
    initial_map, available_dict, required_intersection, initial_laser = read_bff(
        filename)
    initial_laser_path = [(initial_laser[0], initial_laser[1])]
    current_laser_path = initial_laser_path
    sample_history = []

    while check_intersection(current_laser_path, required_intersection):
        current_map = generate_next_map(
            initial_map, available_dict)
        current_laser_path = generate_laser(current_map, initial_laser)

    generate_png(filename, current_map, current_laser_path)
