import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils

from shortest_path_algorithm import *
from student_utils import *
from approximate_TSP import *
from student_utils import *
import random
"""
======================================================================
  Complete the following function.
======================================================================
"""

def getIndices(list_of_locations, list_of_homes, starting_car_location):
    homes = []
    for home in list_of_homes:
        homes += [list_of_locations.index(home)]
    return homes, list_of_locations.index(starting_car_location)

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A list of (location, [homes]) representing drop-offs
    """
    adjacency_matrix = np.array(adjacency_matrix)
    adjacency_matrix[adjacency_matrix=='x'] = -1
    adjacency_matrix = adjacency_matrix.astype(np.float)
    # getIndices is a helper function in solver.py
    homes, start = getIndices(list_of_locations, list_of_homes, starting_car_location)
    # getShortestDistanceMatrix is a helper function in shortest_path_algorithm.py
    shortestPath = getShortestDistanceMatrix(adjacency_matrix, len(list_of_locations))
    initDropOff = set(random.sample(range(0, len(list_of_locations)), len(list_of_homes)))

    # runDescent1 is a helper function in solver.py
    getOptimalDropOff = runDescent1(homes, start, shortestPath, initDropOff)
    # getTSP is a helper function in approximate_TSP.py
    generatePath, cost = getTSP(shortestPath, getOptimalDropOff, start, homes)

    path = [generatePath[0]]
    for i in range(len(generatePath) - 1):
        path += getShortestPathBetween(adjacency_matrix, generatePath[i], generatePath[i + 1])[1:]
    return path, getDropOffs(shortestPath, getOptimalDropOff, homes, list_of_locations)

def getDropOffs(shortest_path, optimal_drop_off, homes, list_of_locations):
    dictionary = {i:set() for i in optimal_drop_off}
    for home in homes:
        minimum = 3 * 10 ** 11
        target = 0
        for drop in optimal_drop_off:
            if (shortest_path[drop][home] < minimum):
                minimum = shortest_path[drop][home]
                target = drop
        dictionary[target].add(home)
    return dictionary

def runDescent1(homes, starting_location, shortest_path, initial_set):
    result = set(initial_set)
    isOver = False
    counter = 0
    total = set(range(0, len(shortest_path)))
    _, currCost = getTSP(shortest_path, result, starting_location, homes)
    while (not isOver and counter < 500):
        isOver = True
        for drop in result:
            result.remove(drop)
            _, cost = getTSP(shortest_path, result, starting_location, homes)
            if (cost < currCost):
                isOver = False
                currCost = cost
                break;
            else:
                result.add(drop)
        if len(result) < len(homes):
            setminus = total.difference(result)
            for toAdd in setminus:
                result.add(toAdd)
                _, cost = getTSP(shortest_path, result, starting_location, homes)
                if (cost < currCost):
                    isOver = False
                    currCost = cost
                    break;
                else:
                    result.remove(toAdd)
        counter += 1
    return result

"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    output_filename = utils.input_to_output(filename)
    output_file = f'{output_directory}/{output_filename}'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
