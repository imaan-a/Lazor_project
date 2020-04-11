def generate_laser(map, initial_laser):
    '''
        Generate the laser path according to map and initial laser condition.

            **Parameters**
                map: *list*
                    2D list representing the map filled with all blocks.
                initial_laser: *list*
                    List of coordinates and direction for each laser to start.

            **Returns**
                current_laser_path: *list, list, tuple*
                    List of all laser paths.
    '''

    def is_in_map(coord):
        if 0 <= coord[0] <= len(map) and 0 <= coord[1] <= len(map[0]):
            return True
        else:
            return False

    def find_next_block(coord, direction_in):
        if map[coord[0]][coord[1]].findtype() == 'vertical':
            next_block = map[coord[0] + direction_in[0]][coord[1]]
        if map[coord[0]][coord[1]].findtype() == 'horizontal':
            next_block = map[coord[0]][coord[1] + direction_in[1]]
        return next_block

    def find_direction_out(coord, direction_in, next_block):
        if is_in_map(next_block.position) is False or next_block.type == 'B':
            direction_out = (0, 0)
        if next_block.type == 'o' or next_block.type == 'x':
            direction_out = direction_in
        if next_block.type == 'A':
            if map[coord[0]][coord[1]].findtype() == 'vertical':
                direction_out = (-direction_in[0], direction_in[1])
            if map[coord[0]][coord[1]].findtype() == 'horizontal':
                direction_out = (direction_in[0], -direction_in[1])
        if next_block.type == 'C':
            if map[coord[0]][coord[1]].findtype() == 'vertical':
                direction_out = [
                    (-direction_in[0], direction_in[1]), direction_in]
            if map[coord[0]][coord[1]].findtype() == 'horizontal':
                direction_out = [
                    (direction_in[0], -direction_in[1]), direction_in]
        return direction_out

    laserlist = []
    direction_list = []
    for i in range(len(initial_laser)):
        laserlist.append([(initial_laser[i][0], initial_laser[i][1])])
        direction_list.append((initial_laser[2], initial_laser[3]))

    N = 0
    while N < len(laserlist):
        laser = laserlist[N]
        initial_direction = direction_list[N]
        while True:
            if len(laser) == 1:
                direction_in = initial_direction
            else:
                direction_in = (laser[-1][0] - laser[-2][0],
                                laser[-1][1] - laser[-2][1])
            direction_out = find_direction_out(
                laser[-1], direction_in, find_next_block(laser[-1], direction_in))
            if find_next_block(laser[-1], direction_in).type == 'C':
                next_coord_0 = laser[-1] + direction_out[0]
                next_coord_1 = laser[-1] + direction_out[1]
                laserlist.append(laser + [next_coord_0])
                laser.append(next_coord_1)
            else:
                next_coord = laser[-1] + direction_out
                laser.append(next_coord)
            if is_in_map(laser[-1]) is False or laser[-1] == laser[-2]:
                laserlist[N] = laser[:-1]
                break
        N += 1

    return laserlist


def check_intersection(laserlist, required_intersection):
    laser_points = []
    for i in laserlist:
        laser_points += i
    result = all(i in laser_points for i in required_intersection)
    return result
