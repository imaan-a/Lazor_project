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


def generate_next_map(map, available_dict, arrangement_history):
    '''
        Genrate next possible map filled with all usable blocks using random
        sampling method.
        The map should be different from all maps generated before.

            **Parameters**
                map: *list, list, object*
                    2D list representing the initial game board.
                available_dict: *dict*
                    Dictionary of quantity of each type of blocks that can be
                    used.
                arrangement_history: *list, dict*
                    List of all previously used blocks arrangement.

            **Returns**
                arrangement: *dict*
                    Dictionary of positions of all blocks that need to be filled.
                next_map: *list, list, object*
                    2D list representing the new map filled with all usable
                    blocks.

    '''
    import random

    def find_arrangement(slots_sample, available_blocks):
        arrangement = {}
        for seq, blocktype in enumerate(available_blocks):
            if blocktype in arrangement.keys():
                arrangement[blocktype].append(slots_sample[seq])
            else:
                arrangement[blocktype] = [slots_sample[seq]]
        return arrangement

    dim_x = len(map)
    dim_y = len(map[0])
    available_slots = [map[i][j].position for i in range(dim_x) for j in range(
        dim_y) if isinstance(map[i][j], Block) and map[i][j].type == 'o']
    available_blocks = []
    for a, b in available_dict.items():
        if b != 0:
            for i in range(b):
                available_blocks.append(a)
    block_num = len(available_blocks)
    next_map = map
    while True:
        slots_sample = random.sample(available_slots, block_num)
        arrangement = find_arrangement(slots_sample, available_blocks)
        if arrangement in arrangement_history:
            continue
        else:
            for i in block_num:
                next_map[slots_sample[i][0]][slots_sample[i]
                                             [1]].type = available_blocks[i]
            break

    return arrangement, next_map
