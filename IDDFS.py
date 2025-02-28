import copy
import time

def move_blank(i,j,n):
    if i+1 < n:
        yield i + 1,j
    if i-1 >= 0:
        yield i - 1,j
    if j+1 < n:
        yield i, j + 1
    if j-1 >= 0:
        yield i, j - 1

def move(state):
    [i, j, grid] = state  # Unpack the current state
    n = len(grid)  # Get the size of the grid

    for pos in move_blank(i, j, n):  # Iterate over possible blank tile moves
        i1, j1 = pos  # New position of the blank tile

        # Swap the blank tile with the target position
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]

        # Yield the new state after the move
        yield [i1, j1, grid]

        # Swap back
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]

def is_goal(state, goal):
    return state == goal


case_1 = [1, 1, [[7, 3, 5], [4, 0, 2], [8, 1, 6]]]
case_2 = [0, 2, [[5, 6, 0], [1, 3, 8], [4, 7, 2]]]
case_3 = [2, 0, [[3, 5, 6], [1, 2, 7], [0, 8, 4]]]
case_4 = [1, 1, [[7, 3, 5], [4, 0, 2], [8, 1, 6]]]
case_5 =  [2, 0, [[6, 4, 8], [7, 1, 3], [0, 2, 5]]]
first_goal = [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]]

case_6 = [0, 0, [[0, 1, 8], [3, 6, 7], [5, 4, 2]]]
case_7 = [2, 0, [[6, 4, 1], [7, 3, 2], [0, 5, 8]]]
case_8 = [0, 0, [[0, 7, 1], [5, 4, 8], [6, 2, 3]]]
case_9 = [0, 2, [[5, 4, 0], [2, 3, 1], [8, 7, 6]]]
case_10 = [2, 1, [[8, 6, 7], [2, 5, 4], [3, 0, 1]]]
second_goal = [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]

# def dfs_rec(path, depth):
#     if is_goal(path[-1], goal):
#         print(f"Goal reached: {path[-1]}")
#         return path
#     if depth <= 0:
#         return None
#
#     else:
#         # may need a copy or deep copy of path[-1]
#         current = copy.deepcopy(path[-1])
#         for next_state in move(current):
#             if next_state not in path:
#                 next_path = path+[next_state]
#                 solution = dfs_rec(next_path, depth-1)
#                 if solution is not None:
#                     return solution
#     return None
#
# def id_dfs_rec(path, max_depth):
#     for depth in range(0, max_depth):
#         solution = dfs_rec(path, depth)
#         if solution is not None:
#             return solution
#
#     return None

#print(id_dfs_rec([case_1], 30))

def state_to_tuple(state):
    i, j, grid = state
    return (i, j, tuple(map(tuple, grid)))

def dfs_rec_with_set(path, visited, depth, goal):
    count = 0
    if is_goal(path[-1], goal):
        #print(f"Goal reached: {path[-1]}")
        return path, count
    if depth <= 0:
        return None, count

    else:
        visited.add(state_to_tuple(path[-1]))
        # may need a copy or deep copy of path[-1]
        current = copy.deepcopy(path[-1])
        for next_state in move(current):
            count +=1
            if state_to_tuple(next_state) not in visited:
                next_path = path+[next_state]
                solution, count = dfs_rec_with_set(next_path, visited, depth-1, goal)
                if solution is not None:
                    return solution, count
    return None, count

def id_dfs_rec_with_set(path, max_depth, goal):
    count = 0
    start = time.time()
    for depth in range(0, max_depth):
        solution, c = dfs_rec_with_set(path, set(), depth, goal)
        count += c
        if solution is not None:
            end = time.time()
            return solution, len(solution) - 1, count, end-start

    end = time.time()
    return None, None, count, end-start

# ID_DFS Cases 1-5, first goal state
# for index, case in enumerate([case_1, case_2, case_3, case_4, case_5]):
#     case_number = index + 1
#     print(id_dfs_rec_with_set([case], 35, case_number, first_goal))
#
# # ID_DFS Cases 1-5, second goal state
# for index, case in enumerate([case_6, case_7, case_8, case_9, case_10]):
#     case_number = index + 6
#     print(id_dfs_rec_with_set([case], 40, case_number, second_goal))

def solve_puzzle(start_state, goal_state):
    path, moves, yields, execution_time = id_dfs_rec_with_set([start_state], 50, goal_state)
    return moves, yields, execution_time, path

for index, case in enumerate([case_1, case_2, case_3, case_4, case_5, case_6, case_7, case_8, case_9, case_10]):
    case_number = index + 1
    goal_state = first_goal if case_number <= 5 else second_goal

    moves, yields, execution_time, path = solve_puzzle(case, goal_state)

    print(
        f"Case Number: {case_number}\n"
        f"Number of moves to solve the case: {len(path) - 1}\n"
        f"Number of nodes opened: {yields}\n"
        f"Computation time: {execution_time} secs\n"
        f"///////////////////////////////////////////////////"
    )

