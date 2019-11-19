import numpy as np

"""
Return the numpy matrix containing the shortest distance between each vertex.
Input adjacency_matrix must be the raw String matrix after data_parser!
"""
def getShortestDistanceMatrix(adjacency_matrix, num_of_locations):
    adjacency_matrix = np.array(adjacency_matrix)
    adjacency_matrix[adjacency_matrix=='x'] = -1
    adjacency_matrix = adjacency_matrix.astype(np.float)
    result = np.zeros(adjacency_matrix.shape)
    for i in range(num_of_locations):
        dist = result[i]
        dist = revisedDjikstra(adjacency_matrix, i, dist, num_of_locations)
        for j in range(num_of_locations):
            result[i, j] = dist[j]
            result[j, i] = dist[j]
    return result
"""
Diiiijjjjjikkkksra's algorithm with some known shortest distances.
"""
def revisedDjikstra(adjacency_matrix, source, dist, num_of_locations):
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
            cost = dist[current] + adjacency_matrix[current, vertex]
            if (cost < dist[vertex]):
                dist[vertex] = cost
    return dist

def getAdjacentUnvisited(current, adjacency_matrix, unVisited):
    return [i for i in unVisited if adjacency_matrix[current, i] > 0]

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
