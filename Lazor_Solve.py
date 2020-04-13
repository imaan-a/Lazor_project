import copy
import itertools
import unittest
import time
from termcolor import cprint
from PIL import Image, ImageDraw

class TestBff(unittest.TestCase):
    '''
    Unit test for all available .bff files. An simple visualization of the solution will be displayed once a test is passed, together with time cost.
    '''
    def test_dark_1(self):
        print('-----------------------------')
        print('Testing dark_1.bff...')
        filename = 'bff/dark_1.bff'
        time_start = time.time()
        board_1, path_1 = solve_bff(filename)
        time_end = time.time()
        time_cost = time_end-time_start
        print('Time cost: %.4fs' % time_cost)
        m, n, initial_1, required_1 = read_bff(filename)
        display_board(board_1.filled, all_laser_points(path_1), initial_1, required_1)


    def test_mad_1(self):
        print('-----------------------------')
        print('Testing mad_1.bff...')
        filename = 'bff/mad_1.bff'
        time_start = time.time()
        board_1, path_1 = solve_bff(filename)
        time_end = time.time()
        time_cost = time_end-time_start
        print('Time cost: %.4fs' % time_cost)
        m, n, initial_1, required_1 = read_bff(filename)
        display_board(board_1.filled, all_laser_points(path_1), initial_1, required_1)

    def test_mad_4(self):
        print('-----------------------------')
        print('Testing mad_4.bff...')
        filename = 'bff/mad_4.bff'
        time_start = time.time()
        board_1, path_1 = solve_bff(filename)
        time_end = time.time()
        time_cost = time_end-time_start
        print('Time cost: %.4fs' % time_cost)
        m, n, initial_1, required_1 = read_bff(filename)
        display_board(board_1.filled, all_laser_points(path_1), initial_1, required_1)

    def test_mad_7(self):
        print('-----------------------------')
        print('Testing mad_7.bff...')
        filename = 'bff/mad_7.bff'
        time_start = time.time()
        board_1, path_1 = solve_bff(filename)
        time_end = time.time()
        time_cost = time_end-time_start
        print('Time cost: %.4fs' % time_cost)
        m, n, initial_1, required_1 = read_bff(filename)
        display_board(board_1.filled, all_laser_points(path_1), initial_1, required_1)

    def test_numbered_6(self):
        print('-----------------------------')
        print('Testing numbered_6.bff...')
        filename = 'bff/numbered_6.bff'
        time_start = time.time()
        board_1, path_1 = solve_bff(filename)
        time_end = time.time()
        time_cost = time_end-time_start
        print('Time cost: %.4fs' % time_cost)
        m, n, initial_1, required_1 = read_bff(filename)
        display_board(board_1.filled, all_laser_points(path_1), initial_1, required_1)

    def test_showstopper_4(self):
        print('-----------------------------')
        print('Testing showstopper_4.bff...')
        filename = 'bff/showstopper_4.bff'
        time_start = time.time()
        board_1, path_1 = solve_bff(filename)
        time_end = time.time()
        time_cost = time_end-time_start
        print('Time cost: %.4fs' % time_cost)
        m, n, initial_1, required_1 = read_bff(filename)
        display_board(board_1.filled, all_laser_points(path_1), initial_1, required_1)

    def test_tiny_5(self):
        print('-----------------------------')
        print('Testing tiny_5.bff...')
        filename = 'bff/tiny_5.bff'
        time_start = time.time()
        board_1, path_1 = solve_bff(filename)
        time_end = time.time()
        time_cost = time_end-time_start
        print('Time cost: %.4fs' % time_cost)
        m, n, initial_1, required_1 = read_bff(filename)
        display_board(board_1.filled, all_laser_points(path_1), initial_1, required_1)

    def test_yarn_5(self):
        print('-----------------------------')
        print('Testing yarn_5.bff...')
        filename = 'bff/yarn_5.bff'
        time_start = time.time()
        board_1, path_1 = solve_bff(filename)
        time_end = time.time()
        time_cost = time_end-time_start
        print('Time cost: %.4fs' % time_cost)
        m, n, initial_1, required_1 = read_bff(filename)
        display_board(board_1.filled, all_laser_points(path_1), initial_1, required_1)


class Block:
    '''
    Class object used for all types of blocks as well as empty block spaces.
    '''
    def __init__(self, position, category):
        self.position = position
        self.category = category

    def findedges(self):
        ''' Returns the four corner coordinates of the block object'''
        return [(self.position[0] + i[0], self.position[1] + i[1])
                for i in [(0, -1), (0, 1), (-1, 0), (1, 0)]]

    def __eq__(self, other):
        if self.position == other.position and self.category == other.category:
            return True
        else:
            return False


class Grid:
    '''
    Class object for grid positions between blocks where blocks do not exist.
    '''
    def __init__(self, position):
        self.position = position

    def findcategory(self):
        '''Returns the direction category of Grid object'''
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


class BoardFiller:
    '''
    Class object with information on specific board arrangement.
    '''
    def __init__(self, initial_board, arrangement_list):
        self.initial_board = initial_board
        self.arrangement_list = arrangement_list
        self.arrangement_history = []
        self.filled = None

    def next(self):
        '''Changes the filled board to another given arrangement'''
        self.arrangement_history.append(self.arrangement_list.pop())
        arrangement_dict = self.arrangement_history[-1]
        self.filled = copy.deepcopy(self.initial_board)
        for loc, cat in arrangement_dict.items():
            for i in range(len(loc)):
                self.filled[loc[i][0]][loc[i][1]].category = cat[i]


class Output:
    '''
    Class used to create and save visual representation of board solution.
    '''

    def __init__(self, solved_board, laser_path, laser_start,
                 intersects, soln_filename):

        self.board = solved_board
        self.name = soln_filename
        xdim = len(self.board[0])
        ydim = len(self.board)
        # create new PIL image
        self.img = Image.new('RGB', (600, 600), (255, 255, 255))
        self.dw = ImageDraw.Draw(self.img)

        # add legend to image
        self.dw.text(
            (20, 40), text="Black Outline - Reflect Block", fill='#000')
        self.dw.text((20, 60), text="Black Square - Opaque Block", fill='#000')
        self.dw.text((20, 80), text="Grey Square - Refract Block", fill='#000')
        self.dw.ellipse([210, 45, 215, 50], fill='#f00')
        self.dw.text((220, 40), text="Lazor Start", fill='#000')
        self.dw.ellipse([210, 65, 215, 70], fill='#000')
        self.dw.text((220, 60), text="Required Intersection", fill='#000')

        # creates visual of board using different block categories
        for j in range(xdim - 1):
            for i in range(ydim - 1):
                c = self.board[i][j]
                if isinstance(c, Block):
                    coords = self.get_coords((i - 1) // 2, (j - 1) // 2)
                    if c.category == 'o':
                        self.add_empty_block(coords)
                    elif c.category == 'A':
                        self.add_reflect_block(coords)
                    elif c.category == 'B':
                        self.add_opaque_block(coords)
                    elif c.category == 'C':
                        self.add_refract_block(coords)

        # displays the laser path on the image
        for n in range(len(laser_path) - 1):
            x1, y1 = laser_path[n]
            x2, y2 = laser_path[n+1]
            if (abs(x1 - x2) <= 1) and (abs(y1 - y2) <= 1):
                coord1 = self.get_laser_coords(x1, y1)
                coord2 = self.get_laser_coords(x2, y2)
                self.add_laser_line(coord1 + coord2)

        for s in laser_start:
            x, y = self.get_laser_coords(s[0], s[1])
            startcoords = [(x - 2, y - 2), (x + 2, y + 2)]
            self.add_start_point(startcoords)
        for r in intersects:
            p, q = r
            new_p, new_q = self.get_laser_coords(p, q)
            requiredcoords = [(new_p - 2, new_q - 2), (new_p + 2, new_q + 2)]
            self.add_required_point(requiredcoords)

        self.save_as_png()

    def add_reflect_block(self, coords):
        '''Adds reflect block type to image at given coordinates.'''
        self.dw.rectangle(coords, outline="#000", fill="#fff", width=4)

    def add_opaque_block(self, coords):
        '''Adds opaque block type to image at given coordinates.'''
        self.dw.rectangle(coords, outline="#000", fill="#000", width=2)

    def add_refract_block(self, coords):
        '''Adds refract block type to image at given coordinates.'''
        self.dw.rectangle(coords, fill="#a5a5a5", outline="#a5a5a5")

    def add_empty_block(self, coords):
        '''Adds empty block type to image at given coordinates.'''
        self.dw.rectangle(coords, outline="#a5a5a5", fill='#fff', width=1)

    def add_laser_line(self, coords):
        '''Adds red line to image at given coordinates to denote laser path.'''
        self.dw.line(coords, fill='#f00', width=2)

    def add_start_point(self, coords):
        '''Adds red circle at given coordinates to denote laser start point.'''
        self.dw.ellipse(coords, fill='#f00')

    def add_required_point(self, coords):
        '''Adds black circle at given coordinates to denote intersection.'''
        self.dw.ellipse(coords, fill='#000')

    def save_as_png(self):
        '''Saves the PIL Image with board drawing as a png file.'''
        self.img.save(self.name + '_soln.png', 'png')

    def get_laser_coords(self, x, y):
        '''Takes board coordinates and scales to image size.'''
        return [28 * x + 27, 28 * y + 107]

    def get_coords(self, i, j):
        '''Takes board coordinates and returns image square coordinates.'''
        coords = [(56 * i + 30, 56 * j + 110), (56 * i + 80, 56 * j + 160)]
        return coords


def display_board(board, laser=[], start=[], required=[]):
    '''
        Print out the given game board for immediate visualization.

            **Parameters**
                board: *list*
                    2D list representing the board filled with all blocks.
                laser: *list, list, tuple*
                    List of lists of coordinates which each laser passes
                    through.
                start: *list, list*
                    List of laser satrting coordinates and directions.
                required: *list, list, tuple*
                    List of coordinates that all lasers need to intersect.

            **Returns**
                None

    '''
    UL, UR, DL, DR = [], [], [], []
    if len(start) != 0:
        for i in start:
            if i[2] == 1 and i[3] == 1:
                DR.append((i[0], i[1]))
            if i[2] == 1 and i[3] == -1:
                UR.append((i[0], i[1]))
            if i[2] == -1 and i[3] == -1:
                UL.append((i[0], i[1]))
            if i[2] == -1 and i[3] == 1:
                DL.append((i[0], i[1]))
    for j in range(len(board[0])):
        for i in range(len(board)):
            c = board[i][j]
            if isinstance(c, Block):
                cprint("%2s" % c.category, 'red', attrs=['bold'], end='')
            elif c.position in laser:
                if c.position in UL: cprint("%2s" % '×', 'green', end='')
                elif c.position in UR: cprint("%2s" % '×', 'green', end='')
                elif c.position in DL: cprint("%2s" % '×', 'green', end='')
                elif c.position in DR: cprint("%2s" % '×', 'green', end='')
                elif c.position in required:
                    cprint("%2s" % '×', 'cyan', end='')
                else:
                    cprint("%2s" % '×', 'magenta', end='')
            else:
                cprint("%2s" % '+', end='')
        print(' ')
    cprint('Red: Block and category', 'red')
    cprint('Green: Laser starting point', 'green')
    cprint('Cyan: Required intersection point', 'cyan')
    cprint('Magenta: Laser point', 'magenta')


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
                Dictionary of quantity of each category of blocks that can be
                used.
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
        '''Transposes given matrix.'''
        a = [[] for i in m[0]]
        for i in m:
            for j in range(len(i)):
                a[j].append(i[j])
        return a
    intersection = [tuple(i) for i in points]

    return trans(grid), usable_blocks, lazors, intersection


def generate_arrangement(initial_board, available_dict):
    '''
        Generate all possible game board arrangements using available blocks.

            **Parameters**
                Initial_board: **list**
                    2D list representing the initial board filled with all
                    preset blocks.
                available_dict: **dict**
                    Dictionary of all usable blocks and their categories.

            **Returns**
                arrangement_list: **list, dict**
                    List of all possible arrangments of usable game blocks.
    '''
    dim_x = len(initial_board)
    dim_y = len(initial_board[0])
    available_slots = [initial_board[i][j].position for i in range(dim_x) for j in range(
        dim_y) if isinstance(initial_board[i][j], Block) and initial_board[i][j].category == 'o']
    available_cats = []
    for a, b in available_dict.items():
        if b != 0:
            for i in range(b):
                available_cats.append(a)
    slots_combinations = list(
        itertools.combinations(available_slots, len(available_cats)))
    cats_permutations = list(
        itertools.permutations(available_cats, len(available_cats)))
    unique_permutations = {i for i in cats_permutations}
    arrangement_list = [{loc: cat}
                        for loc in slots_combinations for cat in unique_permutations]
    return arrangement_list


def generate_laser(board, initial_laser):
    '''
        Generate the laser path according to current game board and initial
        conditions of each laser.

            **Parameters**
                board: **list**
                    2D list representing the board filled with all blocks.
                initial_laser: **list, tuple**
                    List of tuples of coordinates and direction for each laser
                    to start.

            **Returns**
                final_laser_path: **list, list, tuple**
                    List of all laser paths.
    '''

    def is_in_board(coord):
        '''Checks if given coordinates are in range of the board.'''
        if 0 <= coord[0] <= len(board) - 1 and 0 <= coord[1] <= len(board[0]) - 1:
            return True
        else:
            return False

    def find_next_block(coord, direction_in):
        '''Gives coordinates of adjacent block.'''
        if board[coord[0]][coord[1]].findcategory() == 'vertical':
            next_block_coord = (coord[0] + direction_in[0], coord[1])
        if board[coord[0]][coord[1]].findcategory() == 'horizontal':
            next_block_coord = (coord[0], coord[1] + direction_in[1])
        return next_block_coord

    def find_direction_out(coord, direction_in, next_block):
        '''Changes direction of movement based on features of board.'''
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

    def check_cyclic_laser(laser):
        '''Checks if laser forms a loop, returns Boolean.'''
        copy = laser.copy()
        for i in range(len(laser)):
            element = copy.pop()
            index = copy.count(element)
            if index != 0 and copy[-1] == copy[index - 1]:
                return True
        if not copy:
            return False

    final_laser_path = []
    initial_directions = []
    for i in range(len(initial_laser)):
        final_laser_path.append([(initial_laser[i][0], initial_laser[i][1])])
        initial_directions.append((initial_laser[i][2], initial_laser[i][3]))
    current_laser_index = 0
    # Loop over all lasers stored in final_laser_path.
    while current_laser_index < len(final_laser_path):
        laser = final_laser_path[current_laser_index]
        # Build up each laser until it reaches the boundary of map or
        # falls into infinite loop.
        while True:
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
            # Generate the coordinates of next laser point.
            # Fork the current path if next block is refractive.
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
            # When a laser passes through a coordinate which already exists in
            # its path history, current direction should not be the same as the
            # direction when it passed through this coordinate. Otherwise the
            # laser path will never end and need to stop immediately.
            if check_cyclic_laser(laser):
                print('A loop detected in Laser ' + str(current_laser_index))
                final_laser_path[current_laser_index] = laser
                break
        current_laser_index += 1
    return final_laser_path


def check_intersection(laserlist, required_intersection):
    '''
        Checks if all required intersections are in the laser path.

            **Parameters**
                laserlist: **list, tuple**
                    List of laser coordinates in path so far.
                required_intersection: **list, tuple**
                    List of coordinates laser must intersect.

            **Returns**
                result: **bool**
    '''
    result = all(i in all_laser_points(laserlist)
                 for i in required_intersection)
    return result


def all_laser_points(laserlist):
    '''
        Gives laser data as one single list.
    '''
    laser_points = []
    for i in laserlist:
        laser_points += i
    return laser_points


def solve_bff(filename):
    '''
    Solves the lazor game given in bff file.

        **Parameters**
            filename: **str**
                Name of the saved bff file depicting game.
            threshold: **int**
                Maximum length of laser path.

        **Returns**
            current_board: **BoardFiller**
                BoardFiller class object with solved board as attribute.
            current_laser_path: **list, tuple**
                List of coordinates of solved laser path.
    '''
    initial_board, available_dict, initial_laser, required_intersection = read_bff(
        filename)
    initial_laser_path = [[(initial_laser[0][0], initial_laser[0][1])]]
    current_laser_path = initial_laser_path
    arrangement_list = generate_arrangement(initial_board, available_dict)
    current_board = BoardFiller(initial_board, arrangement_list)
    # Generate a new filled game board and calculate laser paths. Check if the
    # lasers could intersect all required points. If not, move to next board
    # until all arrangments are used up.
    while not check_intersection(current_laser_path, required_intersection):
        if current_board.arrangement_list == []:
            raise Exception(
                "Arrangement list elements used up, no solution found.")
        current_board.next()
        current_laser_path = generate_laser(
            current_board.filled, initial_laser)
    return current_board, current_laser_path


if __name__ == '__main__':
    # unittest.main()
    filename = 'bff/mad_1.bff'
    board, path = solve_bff(filename)
    m, n, initial, required = read_bff(filename)
    Output(board.filled, all_laser_points(path), initial, required, filename)
