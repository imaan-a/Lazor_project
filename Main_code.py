from read_and_export import read_bff
from board import generate_next_board
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
        if self.position[0] % 2 == 0 and self.position[1] % 2 == 0:
            return 'prohibited'
        elif self.position[1] % 2 == 0:
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
    initial_board, available_dict, initial_laser, required_intersection = read_bff(
        filename)
    initial_laser_path = [[(initial_laser[0][0], initial_laser[0][1])]]
    current_laser_path = initial_laser_path
    arrangement_history = []

    while not check_intersection(current_laser_path, required_intersection):
        current_arrangement, current_board = generate_next_board(
            initial_board, available_dict, arrangement_history)
        arrangement_history.append(current_arrangement)
        current_laser_path = generate_laser(current_board, initial_laser)

    return current_arrangement, current_laser_path
    # generate_png(filename, current_board, current_laser_path)


if __name__ == '__main__':
    print(solve_bff('mad_1.bff'))
