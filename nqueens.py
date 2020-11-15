import copy
import random


def succ(state, static_x, static_y):
    lists = []
    good_list = []
    n = len(state)
    if state[static_y] != static_x:
        return good_list
    for i in range(n):
        state_cpy = copy.deepcopy(state)
        state_cpy_2 = copy.deepcopy(state)

        if state[i] < len(state) - 1:  # change the position of the queen in the row
            state_cpy[i] += 1
            lists.append(state_cpy)
        if state[i] != 0:
            state_cpy_2[i] -= 1
            lists.append(state_cpy_2)

    for i in range(len(lists)):  # add the successor if it is valid
        if lists[i][static_y] == static_x:
            good_list.append(lists[i])

    return sorted(good_list)


def f(state):
    count = 0
    if state is None:
        return 0
    for i in range(len(state)):
        for j in range(len(state)):
            num_x = state[j]
            num_y = state[i]
            row_diff = abs(num_y - num_x)
            col_diff = abs(j - i)
            if i == j:  # skip the same element
                continue
            if state[i] == state[j]:  # same row
                count += 1
                break
            if row_diff == col_diff:  # check for the diagonals
                count += 1
                break

    return count


def choose_next(curr, static_x, static_y):
    successors = succ(curr, static_x, static_y)
    if len(successors) == 0:
        return
    successors.insert(0, curr)
    successors = sorted(successors)
    list_f = []
    index = 0
    for i in successors:  # get the list of all the f of the successor
        list_f.append(f(i))
    temp = min(list_f)  # find the min f
    for i in range(len(list_f)):  # find which f has the min state
        if temp == list_f[i]:
            index = i
            break
    return successors[index]  # return that successor with the minimum f


def n_queens(initial_state, static_x, static_y):
    previous_f = f(initial_state)
    successor = choose_next(initial_state, static_x, static_y)
    current_f = f(successor)
    if initial_state is not None:
        print(initial_state, "- f=" + str(previous_f))  # print the initial state and the f
    while current_f != previous_f:
        if current_f == 0:
            break
        if successor is not None:  # do not want to print anything if successor is None
            print(successor, "- f=" + str(current_f))
        previous_f = f(successor)
        successor = choose_next(successor, static_x, static_y)  # now find the next best successor of the current state
        current_f = f(successor)
    if successor is not None:
        print(successor, "- f=" + str(current_f))
    return successor


def n_queens_no_print(initial_state, static_x, static_y):  # same method as n_queens but no print statements for restart method
    previous_f = f(initial_state)
    successor = choose_next(initial_state, static_x, static_y)
    current_f = f(successor)
    while current_f != previous_f:
        if current_f == 0:
            break
        previous_f = f(successor)
        successor = choose_next(successor, static_x, static_y)
        current_f = f(successor)
    return successor


def n_queens_restart(n, k, static_x, static_y):
    state = []
    solution = []
    best = []
    final = []
    for i in range(k):
        state = []  # reset the state after finding the best solution for that state
        for j in range(n):  # create a new state
            val = random.randint(0, n - 1)
            state.append(val)
        #state[static_y] = static_x  # make sure that the random state has queen on static x and y
        solution = n_queens_no_print(state, static_x, static_y)
        if solution is None:
            continue
        if len(best) == 0:
            best.append(solution)
        if f(solution) == 0:
            best.clear()
            best.append(solution)
            break
        if len(best) != 0:  # add a state if f is just as good. clear list and add if better
            if f(solution) < f(best[0]):
                best.clear()
                best.append(solution)
            if f(solution) == f(best[0]):
                best.append(solution)
    best = sorted(best)
    for i in range(len(best)):
        print(best[i], "- f=" + str(f(best[i])))


#print(n_queens([0, 1, 2, 3, 5, 6, 6, 7], 0, 0))
#print(n_queens([0, 7, 3, 4, 7, 1, 2, 2], 0, 0))

print(n_queens_restart(8, 1000, 0, 0))
