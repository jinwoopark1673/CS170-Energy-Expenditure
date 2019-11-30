from student_utils import *

#Uses shortest paths with a heuristic to find "good" TA dropoffs
def getCandidate(adj_matrix, dist_matrix, homes, start):

    if len(adj_matrix) != len(dist_matrix):
        print("Error: adjacency matrix and distance matrix are different sizes")
        return

    layer_size = len(adj_matrix)

    T = nx.minimum_spanning_tree(adjacency_matrix_to_graph(adj_matrix)[0])
    num_layers = 2 * T.number_of_edges() # Upper bound for TSP is 2 * MST

    G = nx.Graph()
    G.add_nodes_from(range(layer_size * num_layers))

    #Fill edges:
    for i in range(layer_size):

        dropoff_cost = 0
        #Using Heuristic: drop off all TAs at each stop
        for home in homes:
            dropoff_cost += dist_matrix[i][home]

        for j in range(i + 1, layer_size):
            if adj_matrix[i][j] == 'x':
                continue
            edge_cost = (2 / 3) * adj_matrix[i][j] + dropoff_cost
            for k in range(num_layers - 1):
                u, v = i + layer_size * k, j + layer_size * k
                G.add_edge(u, v + layer_size, weight=edge_cost)
                G.add_edge(v, u + layer_size, weight=edge_cost)

    pred, dist = nx.dijkstra_predecessor_and_distance(G, start)

    best_dropoffs, best_cost = {}, float('inf') #indices of homes
    for k in range(num_layers): #Check all possible path lengths <- This might take a while, but we might be able to shorten it if we had an estimate of the optimal route length (in # edges)
        end = start + layer_size * k
        if end not in pred:
            continue

        path = [start]
        while end != start:
            end = pred[end][0]
            path.append(end % layer_size)

        #We have a path; now to find best TA dropoffs along this path
        dropoffs, cost = {}, 0
        for home in homes:
            dropoff = min(path, key=lambda place: dist_matrix[place][home])
            cost += dist_matrix[dropoff][home]
            if dropoff in dropoffs:
                dropoffs[dropoff].append(home)
            else:
                dropoffs[dropoff] = [home]

        if cost < best_cost:
            best_dropoffs, best_cost = dropoffs, cost
    return best_dropoffs #A dictionary that looks like {place:[TA homes]}

def brian_tests():
    adj_matrix = [ ['x', 1,   2,   'x', 'x', 'x', 'x'],
                   [1,   'x', 'x', 1,   'x', 'x', 'x'],
                   [2,   'x', 'x', 2,   'x', 'x', 'x'],
                   ['x', 1,   2,   'x', 2,   1,   'x'],
                   ['x', 'x', 'x', 2,   'x', 'x', 2  ],
                   ['x', 'x', 'x', 1,   'x', 'x', 1  ],
                   ['x', 'x', 'x', 'x', 2,   1,   'x'], ]
    pred_matrix, dist_matrix = nx.floyd_warshall_predecessor_and_distance(adjacency_matrix_to_graph(adj_matrix)[0])
    #print(distance[0])
    #print(pred[0])

    print(getCandidate(adj_matrix, dist_matrix, [2, 4], 0))
    return
