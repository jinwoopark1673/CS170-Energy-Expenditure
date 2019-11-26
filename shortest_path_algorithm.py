import numpy as np

"""
Return the numpy matrix containing the shortest distance between each vertex.
Input adjacency_matrix must be the raw String matrix after data_parser!
"""
def getShortestDistanceMatrix(adjacency_matrix, num_of_locations):
    result = np.zeros(adjacency_matrix.shape)
    for i in range(num_of_locations):
        dist = result[i]
        dist = revisedDijkstra(adjacency_matrix, i, dist, num_of_locations)
        for j in range(num_of_locations):
            result[i, j] = dist[j]
            result[j, i] = dist[j]
    return result

"""
Diiiijjjjjkkkkstra's algorithm with some known shortest distances.
"""
def revisedDijkstra(adjacency_matrix, source, dist, num_of_locations):
    unVisited = set()
    for i in range(num_of_locations):
        if (dist[i] == 0 and i != source):
            dist[i] = 3 * 10 ** 11
        unVisited.add(i)
    while (len(unVisited) != 0):
        current = getArgminDist(dist, unVisited)
        unVisited.remove(current)
        toVisit = getAdjacentUnvisited(current, adjacency_matrix, unVisited)
        for vertex in toVisit:
            cost = dist[current] + adjacency_matrix[current][vertex]
            if (cost < dist[vertex]):
                dist[vertex] = cost
    return dist

def getAdjacentUnvisited(current, adjacency_matrix, unVisited):
    return [i for i in unVisited if adjacency_matrix[current][i] > 0]

def getArgminDist(dist, unVisited):
    minValue = 3 * 10 ** 11
    minIndex = 0
    for s in unVisited:
        minIndex = s
        break;
    for vertex in unVisited:
        if (dist[vertex] < minValue):
            minValue = dist[vertex]
            minIndex = vertex
    return minIndex

"""
Basic Diiiiiijkkkkkkkkssssssssssstra for finding the shortest path between two points
"""
def getShortestPathBetween(adjacency_matrix, v1, v2):
    unVisited = set()
    dist = [0] * len(adjacency_matrix)
    previous = [-1] * len(adjacency_matrix)
    for i in range(len(adjacency_matrix)):
        if (i != v1):
            dist[i] = 3 * 10 ** 11
        unVisited.add(i)
    while (len(unVisited) != 0):
        current = getArgminDist(dist, unVisited)
        unVisited.remove(current)
        toVisit = getAdjacentUnvisited(current, adjacency_matrix, unVisited)
        for vertex in toVisit:
            cost = dist[current] + adjacency_matrix[current][vertex]
            if (cost < dist[vertex]):
                dist[vertex] = cost
                previous[vertex] = current
    found = v2
    result = [v2]
    while (found != v1):
        result += [previous[found]]
        found = previous[found]
    return result[::-1]

def getShortestPathsBetween(adjacency_matrix, start, homes):
    unVisited = set()
    dist = [0] * len(adjacency_matrix)
    previous = [-1] * len(adjacency_matrix)
    for i in range(len(adjacency_matrix)):
        if (i != start):
            dist[i] = 3 * 10 ** 11
        unVisited.add(i)
    while (len(unVisited) != 0):
        current = getArgminDist(dist, unVisited)
        unVisited.remove(current)
        toVisit = getAdjacentUnvisited(current, adjacency_matrix, unVisited)
        for vertex in toVisit:
            cost = dist[current] + adjacency_matrix[current][vertex]
            if (cost < dist[vertex]):
                dist[vertex] = cost
                previous[vertex] = current
    result = []
    costs = []
    for home in homes:
        cost = 0
        found = home
        path = [home]
        while (found != start):
            path += [previous[found]]
            found = previous[found]
            cost += adjacency_matrix[found][previous[found]]
        result += [path[::-1]]
        costs += [cost]
    return result, costs

def getTwoAndFifthStations(adjacency_matrix, start, homes):
    paths, costs = getShortestPathsBetween(adjacency_matrix, start, homes)
    result = set()
    for i in range(len(paths)):
        path = paths[i]
        cost = costs[i] * 2 / 5
        currentCost = 0
        for j in range(len(path) - 1):
            currentCost += adjacency_matrix[path[j]][path[j + 1]]
            if (currentCost >= cost):
                result.add(path[j])
                break;
    return result
