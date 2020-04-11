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


def generate_laser(board, initial_laser):
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
        if 0 <= coord[0] <= len(board) and 0 <= coord[1] <= len(board[0]):
            return True
        else:
            return False

    def find_next_block(coord, direction_in):
        if board[coord[0]][coord[1]].findtype() == 'prohibited' or is_in_board(coord) is False or isinstance(board[coord[0]][coord[1]], Block):
            raise Exception('Current coord is prohibited:' + str(coord))
        if board[coord[0]][coord[1]].findtype() == 'vertical':
            next_block = board[coord[0] + direction_in[0]][coord[1]]
        if board[coord[0]][coord[1]].findtype() == 'horizontal':
            next_block = board[coord[0]][coord[1] + direction_in[1]]
        return next_block

    def find_direction_out(board, coord, direction_in, next_block):
        if board[coord[0]][coord[1]].findtype() == 'prohibited' or is_in_board(coord) is False or isinstance(board[coord[0]][coord[1]], Block):
            raise Exception('Current coord is prohibited:' + str(coord))
        if is_in_board(next_block.position) is False or next_block.type == 'B':
            direction_out = (0, 0)
        if next_block.type == 'o' or next_block.type == 'x':
            direction_out = direction_in
        if next_block.type == 'A':
            if board[coord[0]][coord[1]].findtype() == 'vertical':
                direction_out = (-direction_in[0], direction_in[1])
            if board[coord[0]][coord[1]].findtype() == 'horizontal':
                direction_out = (direction_in[0], -direction_in[1])
        if next_block.type == 'C':
            if board[coord[0]][coord[1]].findtype() == 'vertical':
                direction_out = [
                    (-direction_in[0], direction_in[1]), direction_in]
            if board[coord[0]][coord[1]].findtype() == 'horizontal':
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
        initial_direction = initial_directions[current_laser_index]
        # Start an infinite loop for laser path propagation.
        while True:
            if len(laser) == 1:
                direction_in = initial_direction
            else:
                direction_in = (laser[-1][0] - laser[-2][0],
                                laser[-1][1] - laser[-2][1])
            direction_out = find_direction_out(
                board, laser[-1], direction_in, find_next_block(laser[-1], direction_in))
            if find_next_block(laser[-1], direction_in).type == 'C':
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
            # If laser has reached its end, break the loop.
            if is_in_board(laser[-1]) is False or laser[-1] == laser[-2]:
                final_laser_path[current_laser_index] = laser[:-1]
                break
        current_laser_index += 1

    return final_laser_path


def check_intersection(laserlist, required_intersection):
    laser_points = []
    for i in laserlist:
        laser_points += i
    result = all(i in laser_points for i in required_intersection)
    return result
