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

    return trans(grid), usable_blocks, lazors, points


if __name__ == '__main__':
    board, dict1, laser, points = read_bff('mad_1.bff')
