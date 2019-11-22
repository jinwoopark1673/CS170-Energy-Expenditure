"""
shortest_path produced from shortest_path_algorithm.py
drop_locations is a list of indices of drop locations
initial_location is the index of the starting point
homes is a set of indices of TA homes
"""
def getTSP(shortest_path, drop_locations, initial_location, homes):
    cycle = nearestNN(shortest_path, drop_locations, initial_location)
    #cycle = opt2Exchange(shortest_path, nearestNN(shortest_path, drop_locations, initial_location))
    return cycle, computeCost(shortest_path, cycle, homes, drop_locations)

def nearestNN(shortest_path, drop_locations, initial_location):
    result = [initial_location]
    history = set(drop_locations)
    current = initial_location
    history.discard(current)
    while (len(history) > 0):
        minimum = 3 * 10 ** 11
        argmin = 0
        for vertex in history:
            if (minimum > shortest_path[current][vertex]):
                minimum = shortest_path[current][vertex]
                argmin = vertex
        current = argmin
        history.remove(current)
        result += [current]
    return result + [initial_location]

def opt2Exchange(shortest_path, cycle):
    cycleLength = len(cycle)
    isOver = False
    while (not isOver):
        isOver = True
        for i in range(1, cycleLength - 1):
            for j in range(i + 1, cycleLength - 1):
                random1 = i
                random2 = j
                if ((random1 + 1 != random2) and i != j):
                    currCost = shortest_path[cycle[random1]][cycle[random1 + 1]] + shortest_path[cycle[random2]][cycle[random2 + 1]]
                    switchCost = shortest_path[cycle[random1]][cycle[random2]] + shortest_path[cycle[random1 + 1]][cycle[random2 + 1]]
                    if (switchCost < currCost):
                        cycle[random1 + 1:random2 + 1] = cycle[random1 + 1:random2 + 1][::-1]
                        isOver = False
    return cycle

def computeCost(shortest_path, cycle, homes, drop_locations):
    result = 0
    for i in range(len(cycle) - 1):
        result += shortest_path[cycle[i]][cycle[i + 1]]
    for home in homes:
        minimum = 3 * 10 ** 11
        for drop in drop_locations:
            if (shortest_path[drop][home] < minimum):
                minimum = shortest_path[drop][home]
        result += minimum
    return result
