def generate_next(map, available_dict, map_history):
    '''
        Genrate next possible map filled with all usable blocks.
        The map should be different from all previous maps in map_history.

            **Parameters**
                initial_map: *list*
                    2D list representing the initial game board.
                available_dict: *dict*
                    Dictionary of quantity of each type of blocks that can be
                    used.
                map_history: *list*
                    List of all previously used maps.

            **Returns**
                next_map: *list*
                    2D list representing the new map filled with all usable
                    blocks.
    '''
    import random
    dim_x = len(map)
    dim_y = len(map[0])
    available_slots = [map[i][j].position for i in range(dim_x) for j in range(
        dim_y) if isinstance(map[i][j], Block) and map[i][j].type == 'o']
    available_blocks = [
        a for a in available_dict.keys for b in range(available_dict[a])]
    block_num = len(available_blocks)
    next_map = map
    while 1 == 1:
        slots_sample = random.sample(available_slots, block_num)
        for i in block_num:
            next_map[slots_sample[i][0]][slots_sample[i][1]].type = available_blocks[i]
        if next_map not in map_history:
            map_history.append(next_map)
            break
    return next_map
