import numpy as np
import math

def get_average_money(n, s, o_location, fp, start_location, end_location):
    for index in range(n):
        total = 0.0
        utility_grid = create_utility_grid(s, o_location, end_location, index)
        grid = create_grid(utility_grid, s)
        for number in range(10):
            total += get_money_earned(s, index, grid, number, o_location, start_location, end_location)
        sum_total = int(math.floor(total / 10.0))
        fp.write(str(sum_total) + "\n")

def create_utility_grid(s, o_location, end_location, index):
    utility_grid = []
    for i in range(s):
        col = [-1.0] * s
        utility_grid.append(col)

    for i in o_location:
        utility_grid[i[0]][i[1]] -= 100.0

    utility_grid[end_location[index][0]][end_location[index][1]] += 100
    print(utility_grid)
    return value_iteration(index, utility_grid, o_location, end_location, s)

def value_iteration(index, utility_grid, o_location, end_location, s):
    while True:
        temp = []
        for i in range(s):
            col = [0.0] * s
            temp.append(col)
        max_diff = 0.0
        for col in range(s):
            for row in range(s):
                if (col, row) == end_location[index]:
                    temp[col][row] = 99.0
                    continue

                if col < 0 or col >= s or row - 1 < 0 or row - 1 >= s:  north_utility = utility_grid[col][row]
                else:   north_utility = utility_grid[col][row - 1]
                if col < 0 or col >= s or row + 1 < 0 or row + 1 >= s:  south_utility = utility_grid[col][row]
                else:   south_utility = utility_grid[col][row + 1]
                if col + 1 < 0 or col + 1 >= s or row < 0 or row >= s:  east_utility = utility_grid[col][row]
                else:   east_utility = utility_grid[col + 1][row]
                if col - 1 < 0 or col - 1 >= s or row < 0 or row >= s:  west_utility = utility_grid[col][row]
                else:   west_utility = utility_grid[col - 1][row]

                north = 0.7 * north_utility + 0.1 * (south_utility + west_utility + east_utility)
                south = 0.7 * south_utility + 0.1 * (north_utility + west_utility + east_utility)
                east = 0.7 * east_utility + 0.1 * (south_utility + west_utility + north_utility)
                west = 0.7 * west_utility + 0.1 * (south_utility + north_utility + east_utility)
                max_utility = max(north, south, east, west)

                if (col, row) in o_location:        points = -101.0
                elif (col, row) == end_location[index]:     points = 99.0
                else:       points =  -1.0
                new_utility = points + 0.90 * max_utility
                temp[col][row] = new_utility
                current_diff = abs(new_utility - utility_grid[col][row])
                if current_diff > max_diff:  max_diff = current_diff
        if max_diff < 0.1:  break
        utility_grid = temp
    return utility_grid

def create_grid(utility_grid, s):
    grid = []
    for i in range(s):
        col = [0] * s
        grid.append(col)

    for col in range(s):
        for row in range(s):
            grid[col][row] = get_best_move(col, row, utility_grid, s)
    print(grid)
    return grid

def get_best_move(col, row, utility_grid, s):
    direction = ["W", "E", "S", "N"]
    best_move = ""
    max_utility = None

    if col < 0 or col >= s or row + 1 < 0 or row + 1 >= s:  north_utility = utility_grid[col][row]
    else:   north_utility = utility_grid[col][row + 1]

    if col < 0 or col >= s or row - 1 < 0 or row - 1 >= s:  south_utility = utility_grid[col][row]
    else:   south_utility = utility_grid[col][row - 1]

    if col + 1 < 0 or col + 1 >= s or row < 0 or row >= s:  east_utility = utility_grid[col][row]
    else:   east_utility = utility_grid[col + 1][row]

    if col - 1 < 0 or col - 1 >= s or row < 0 or row >= s:  west_utility = utility_grid[col][row]
    else:   west_utility = utility_grid[col - 1][row]


    for dir in direction:
        if dir == "W":      utility = 0.7 * west_utility + 0.1 * (south_utility + north_utility + east_utility)
        elif dir == "E":    utility = 0.7 * east_utility + 0.1 * (south_utility + west_utility + north_utility)
        elif dir == "S":    utility = 0.7 * south_utility + 0.1 * (north_utility + west_utility + east_utility)
        else:   utility = 0.7 * north_utility + 0.1 * (south_utility + west_utility + east_utility)
        if max_utility is None or utility > max_utility:
            max_utility = utility
            best_move = dir
        elif max_utility == utility:
            best_move = dir

    return best_move

def get_money_earned(s, index, grid, number, o_location, start_location, end_location):
    current_location = start_location[index]
    if current_location == end_location[index]:
        return 99.0
    money = 0.0
    np.random.seed(number)
    swerve = np.random.random_sample(1000000)
    count = 0
    while current_location != end_location[index]:
        best_move = grid[current_location[0]][current_location[1]]
        if swerve[count] > 0.7:
            if swerve[count] > 0.8:
                if swerve[count] > 0.9:
                    best_move = turn_left(turn_left(best_move))
                else:
                    best_move = turn_left(best_move)
            else:
                best_move = turn_right(best_move)
        current_location = get_next_location(s, current_location, best_move)
        money -= 1.0
        if current_location in o_location:  money -= 100.0
        count += 1
    money += 100.0
    print(money)
    return money

def turn_left(move):
    if move == "N":     return "W"
    elif move == "S":   return "E"
    elif move == "E":   return "N"
    elif move == "W":   return "S"

def turn_right(move):
    if move == "N":     return "E"
    elif move == "S":   return "W"
    elif move == "E":   return "S"
    elif move == "W":   return "N"

def get_next_location(s, current_location, actual_move):
    if actual_move == "N":      next_location = (current_location[0], current_location[1] + 1)
    elif actual_move == "S":    next_location = (current_location[0], current_location[1] - 1)
    elif actual_move == "W":    next_location = (current_location[0] - 1, current_location[1])
    else:   next_location = (current_location[0] + 1, current_location[1])

    if next_location[0] < 0 or next_location[0] >= s or next_location[1] < 0 or next_location[1] >= s:      return current_location
    else:   return next_location

def main():
    f = open("input5.txt")
    fp = open("output.txt", "w")
    s = int((f.readline()).strip('\n'))
    n = int((f.readline()).strip('\n'))
    o = int((f.readline()).strip('\n'))
    o_location = []
    start_location = []
    end_location = []
    for _ in range(o):
        x = ((f.readline()).strip('\n')).split(",")
        (a, b) = (int(x[0]), int(x[1]))
        o_location.append((a,b))
    for _ in range(n):
        x = ((f.readline()).strip('\n')).split(",")
        (a, b) = (int(x[0]), int(x[1]))
        start_location.append((a,b))
    for _ in range(n):
        x = ((f.readline()).strip('\n')).split(",")
        (a, b) = (int(x[0]), int(x[1]))
        end_location.append((a,b))
    print(o_location, start_location, end_location)

    get_average_money(n, s, o_location, fp, start_location, end_location)
    f.close()
    fp.close()

main()