import copy
import itertools
from termcolor import cprint
from PIL import Image, ImageDraw

class Block:
    def __init__(self, position, category):
        self.position = position
        self.category = category

    def findedges(self):
        return [(self.position[0] + i[0], self.position[1] + i[1]) for i in [(0, -1), (0, 1), (-1, 0), (1, 0)]]

    def __eq__(self, other):
        if self.position == other.position and self.category == other.category:
            return True
        else:
            return False


class Grid:
    def __init__(self, position):
        self.position = position

    def findcategory(self):
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


class Board_filler:
    def __init__(self, initial_board, arrangement_list, available_list):
        self.initial_board = initial_board
        self.arrangement_list = arrangement_list
        self.arrangement_history = []
        self.available_list = available_list
        self.filled = 0

    def next(self):
        self.arrangement_history.append(self.arrangement_list.pop())
        arrangement = self.arrangement_history[-1]
        self.filled = copy.deepcopy(self.initial_board)
        for i in range(len(self.available_list)):
            self.filled[arrangement[i][0]][arrangement[i]
                                           [1]].category = self.available_list[i]

class Output:
    
    def __init__(self, solved_board, soln_filename):
        
        self.img = Image.new('RGB', (800, 800), (255,255,255))
        self.dw = ImageDraw.Draw(self.img)
        self.board = solved_board
        self.name = soln_filename
        self.xdim = len(self.board[0])
        self.ydim = len(self.board)
        
        self.dw.text((20, 40), text="Black Outline - Reflect Block", fill='#000')
        self.dw.text((20, 60), text="Black Square - Opaque Block", fill='#000')
        self.dw.text((20, 80), text="Grey Square - Refract Block", fill='#000')
        
        for x in range(self.xdim):
            for y in range(self.ydim):
                coords = self.get_coords(x, y)
                c = self.board[x][y]
                if isinstance(c, Block):
                    if c.category == 'o':
                        self.add_empty_block(coords)
                    elif c.category == 'A':
                        self.add_reflect_block(coords)
                    elif c.category == 'B':
                        self.add_opaque_block(coords)
                    elif c.category == 'C':
                        self.add_refract_block(coords)
        self.save_as_png()

    def add_reflect_block(self, coords):
        self.dw.rectangle(coords, outline = "#000", fill = "#fff", width=4)
    
    def add_opaque_block(self, coords):
        self.dw.rectangle(coords, outline="#000", fill="#000", width=2)
    
    def add_refract_block(self, coords):
        self.dw.rectangle(coords, fill="#a5a5a5", outline="#a5a5a5")
    
    def add_empty_block(self, coords):
        self.dw.rectangle(coords, outline="#a5a5a5", fill='#fff', width=1)
    
    def save_as_png(self):
        self.img.save(self.name + '.png', 'png')
    
    def get_coords(self, x, y):
        coords = [(70 * x + 30, 70 * y + 110), (70 * x + 80, 70 * y + 160)]
        return coords
    
def display_board(board, laser=[]):
    for i in range(len(board)):
        for j in range(len(board[1])):
            c = board[j][i]
            if isinstance(c, Block):
                cprint(c.category, 'green', end=' ')
            elif c.position in laser:
                cprint('*', 'red', end = ' ')
            else:
                cprint('*', end=' ')
        print(' ')


def read_bff(filename):
    '''
    Extracts necessary data on lazor level from .bff file.

        **Parameters**
            filename: *str*
                Name of bff file to be read.

        **Returns**
            grid: *list, list, object*
                2D list of class instances representing the initial game board.
            usable_blocks: *dict*
                Dictionary of quantity of each category of blocks that can be used.
            lazors: *list, tuple*
                List of coordinates and direction for each lazor.
            points: *list, tuple*
                List of coordinates that lazors need to intersect.
    '''
    file = open(filename, 'r')
    contents = []
    for line in file:
        stripped = line.strip()
        contents.append(stripped)
    file.close()
    ind1 = contents.index('GRID START')
    ind2 = contents.index('GRID STOP')
    vals = []
    for row in contents[ind1 + 1:ind2]:
        row = list(row.replace(' ', ''))
        vals.append(row)
    contents = contents[ind2 + 1:]
    xlen = len(vals[0])
    grid = [[0 for i in range(2 * xlen + 1)]
            for j in range(2 * (ind2 - ind1) - 1)]
    for x in range(2 * xlen + 1):
        for y in range(len(grid)):
            if (x % 2) == 0 or (y % 2) == 0:
                grid[y][x] = Grid((x, y))
            else:
                block_category = vals[(y - 1) // 2][(x - 1) // 2]
                grid[y][x] = Block((x, y), block_category)
    A = 0
    B = 0
    C = 0
    lazors = []
    points = []
    for line in contents:
        if 'A' in line:
            A = int(line[-1])
        if 'B' in line:
            B = int(line[-1])
        if 'C' in line:
            C = int(line[-1])
        if 'L' in line:
            lazors.append([int(x) for x in line.split(' ')[1:]])
        if 'P' in line:
            points.append([int(x) for x in line.split(' ')[1:]])

    usable_blocks = {'A': A, 'B': B, 'C': C}

    def trans(m):
        a = [[] for i in m[0]]
        for i in m:
            for j in range(len(i)):
                a[j].append(i[j])
        return a
    intersection = [tuple(i) for i in points]

    return trans(grid), usable_blocks, lazors, intersection


def generate_laser(board, initial_laser, threshold_1, threshold_2):
    '''
        Generate the laser path according to board and initial laser condition.

            **Parameters**
                board: *list*
                    2D list representing the board filled with all blocks.
                initial_laser: *list, tuple*
                    List of tuples of coordinates and direction for each laser
                    to start.

            **Returns**
                final_laser_path: *list, list, tuple*
                    List of all laser paths.
    '''

    def is_in_board(coord):
        if 0 <= coord[0] <= len(board) - 1 and 0 <= coord[1] <= len(board[0]) - 1:
            return True
        else:
            return False

    def find_next_block(coord, direction_in):
        if board[coord[0]][coord[1]].findcategory() == 'vertical':
            next_block_coord = (coord[0] + direction_in[0], coord[1])
        if board[coord[0]][coord[1]].findcategory() == 'horizontal':
            next_block_coord = (coord[0], coord[1] + direction_in[1])
        return next_block_coord

    def find_direction_out(coord, direction_in, next_block):
        if next_block.category == 'B':
            direction_out = (0, 0)
        if next_block.category == 'o' or next_block.category == 'x':
            direction_out = direction_in
        if next_block.category == 'A':
            if board[coord[0]][coord[1]].findcategory() == 'vertical':
                direction_out = (-direction_in[0], direction_in[1])
            if board[coord[0]][coord[1]].findcategory() == 'horizontal':
                direction_out = (direction_in[0], -direction_in[1])
        if next_block.category == 'C':
            if board[coord[0]][coord[1]].findcategory() == 'vertical':
                direction_out = [
                    (-direction_in[0], direction_in[1]), direction_in]
            if board[coord[0]][coord[1]].findcategory() == 'horizontal':
                direction_out = [
                    (direction_in[0], -direction_in[1]), direction_in]
        return direction_out

    final_laser_path = []
    initial_directions = []
    for i in range(len(initial_laser)):
        final_laser_path.append([(initial_laser[i][0], initial_laser[i][1])])
        initial_directions.append((initial_laser[i][2], initial_laser[i][3]))
    current_laser_index = 0

    while current_laser_index < len(final_laser_path):
        laser = final_laser_path[current_laser_index]
        while current_laser_index < threshold_1:
            if len(laser) == 1:
                direction_in = initial_directions[current_laser_index]
            else:
                direction_in = (laser[-1][0] - laser[-2][0],
                                laser[-1][1] - laser[-2][1])
            next_block_coord = find_next_block(laser[-1], direction_in)
            if is_in_board(next_block_coord) is False:
                final_laser_path[current_laser_index] = laser
                break
            next_block = board[next_block_coord[0]][next_block_coord[1]]
            direction_out = find_direction_out(
                laser[-1], direction_in, next_block)
            if next_block.category == 'C':
                next_coord_0 = (laser[-1][0] + direction_out[0][0],
                                laser[-1][1] + direction_out[0][1])
                next_coord_1 = (laser[-1][0] + direction_out[1][0],
                                laser[-1][1] + direction_out[1][1])
                final_laser_path.append(laser + [next_coord_0])
                laser.append(next_coord_1)
            else:
                next_coord = (laser[-1][0] + direction_out[0],
                              laser[-1][1] + direction_out[1])
                laser.append(next_coord)
            if is_in_board(laser[-1]) is False or laser[-1] == laser[-2]:
                final_laser_path[current_laser_index] = laser[:-1]
                break
            elif len(laser) > threshold_2:
                final_laser_path[current_laser_index] = laser
                break
        current_laser_index += 1

    return final_laser_path


def check_intersection(laserlist, required_intersection):
    result = all(i in all_laser_points(laserlist) for i in required_intersection)
    return result

def all_laser_points(laserlist):
    laser_points = []
    for i in laserlist:
        laser_points += i
    return laser_points

def solve_bff(filename, threshold_1, threshold_2):
    initial_board, available_dict, initial_laser, required_intersection = read_bff(
        filename)
    initial_laser_path = [[(initial_laser[0][0], initial_laser[0][1])]]
    current_laser_path = initial_laser_path
    dim_x = len(initial_board)
    dim_y = len(initial_board[0])
    available_slots = [initial_board[i][j].position for i in range(dim_x) for j in range(
        dim_y) if isinstance(initial_board[i][j], Block) and initial_board[i][j].category == 'o']
    available_list = []
    for a, b in available_dict.items():
        if b != 0:
            for i in range(b):
                available_list.append(a)
    arrangement_list = list(
        itertools.permutations(available_slots, len(available_list)))
    current_board = Board_filler(
        initial_board, arrangement_list, available_list)

    while not check_intersection(current_laser_path, required_intersection):
        current_board.next()
        current_laser_path = generate_laser(
            current_board.filled, initial_laser, threshold_1, threshold_2)
        if current_board.arrangement_list == []:
            print("Arrangement list elements used up.")
            break

    return current_board, current_laser_path
    # generate_png(filename, current_board, current_laser_path)


if __name__ == '__main__':
    board_1, path_1 = solve_bff('bff/yarn_5.bff', 1, 70)
    display_board(board_1.filled, all_laser_points(path_1))
    Output(board_1.filled, '_soln')

