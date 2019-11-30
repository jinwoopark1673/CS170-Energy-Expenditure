import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import time

from shortest_path_algorithm import *
from student_utils import *
from approximate_TSP import *
from epic_gamer_code import *
import random
"""
======================================================================
  Complete the following function.
======================================================================
"""

def getCandidates(adjacency_matrix, shortest_path, homes, start):
    candidates = []
    candidates += [set(homes)]
    if len(adjacency_matrix) <= 100:
        candidates += [set(getCandidate(adjacency_matrix, shortest_path, homes, start).keys())]
    return candidates

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
    # matrix to index form where invalid edge has weight -1
    adjacency_matrix = np.array(adjacency_matrix)
    adjacency_matrix[adjacency_matrix=='x'] = -1
    adjacency_matrix = adjacency_matrix.astype(np.float)
    # getIndices is a helper function in solver.py
    homes, start = getIndices(list_of_locations, list_of_homes, starting_car_location)
    # getShortestDistanceMatrix is a helper function in shortest_path_algorithm.py
    shortestPath = getShortestDistanceMatrix(adjacency_matrix, len(list_of_locations))

    dropOffCandidates = getCandidates(adjacency_matrix, shortestPath, homes, start)

    minimum = 3 * 10 ** 15
    finalPath = []
    finalDropOff = set()

    """
    Descent2 takes very long time for 100.in and 200.in case.
    Descent1 is pretty fast for all three input types.
    """
    if (len(list_of_locations) <= 100): # Descent2
        finalDropOff, finalPath, minimum = runDescent([dropOffCandidates[0]], runDescent2, homes, start, shortestPath, minimum, finalPath, finalDropOff, 3000)
    if (len(list_of_locations) <= 200): # Descent12Mix
        finalDropOff, finalPath, minimum = runDescent(dropOffCandidates, runDescent12Mix, homes, start, shortestPath, minimum, finalPath, finalDropOff, 3000)
    finalDictionary = getDropOffs(shortestPath, finalDropOff, homes, list_of_locations)

    # Get rid of drop off locations with 0 TA
    keySet = set(finalDictionary.keys())
    for key in keySet:
        if (len(finalDictionary[key]) == 0):
            finalDictionary.pop(key, None)

    path = [finalPath[0]]
    for i in range(len(finalPath) - 1):
        path += getShortestPathBetween(adjacency_matrix, finalPath[i], finalPath[i + 1])[1:]
    return path, finalDictionary

def runDescent(candidates, descent_function, homes, start, shortestPath, minimum, optimalPath, optimalDropOff, num_iterations):
    for candidate in candidates:
        getOptimalDropOff = descent_function(homes, start, shortestPath, candidate, 3000)
        generatePath, cost = getTSPfast(shortestPath, getOptimalDropOff, start, homes)
        # TODO
        # generatePath, cost = getTSPslow(shortestPath, getOptimalDropOff, start, homes)
        if (cost < minimum):
            minimum = cost
            optimalPath = generatePath
            optimalDropOff = getOptimalDropOff
    return optimalDropOff, optimalPath, minimum

def getIndices(list_of_locations, list_of_homes, starting_car_location):
    """
    Given a list of locations, homes, and initial car location,
    return a new list containing corresponding indices of homes
    and the index of the initial location.
    """
    homes = []
    for home in list_of_homes:
        homes += [list_of_locations.index(home)]
    return homes, list_of_locations.index(starting_car_location)

def getDropOffs(shortest_path, optimal_drop_off, homes, list_of_locations):
    """
    Get optimal dropoff locations of TAs given a set of drop off locations and a list of homes
    """
    dictionary = {i:set() for i in optimal_drop_off}
    for home in homes:
        minimum = 3 * 10 ** 15
        target = 0
        for drop in optimal_drop_off:
            if (shortest_path[drop][home] < minimum):
                minimum = shortest_path[drop][home]
                target = drop
        dictionary[target].add(home)
    return dictionary

def runDescent1(homes, starting_location, shortest_path, initial_set, num_iterations):
    """
    Run Descent1 algorithm on the given set of drop off locations.
    Descent1 checks whether removing or adding a vertex produce a better cost
    and makes a descent until convergence.
    An iteration runs in O(n) * O(TSP).
    """
    result = set(initial_set)
    counter = 0
    total = set(range(0, len(shortest_path)))
    while (counter < num_iterations):
        _, currCost = getTSPfast(shortest_path, result, starting_location, homes)
        nabla = 0
        nabla_arg = set()
        if (len(result) > 1):
            for drop in list(result):
                if (len(result) > 1):
                    result.remove(drop)
                    _, cost = getTSPfast(shortest_path, result, starting_location, homes)
                    if (currCost - cost > nabla):
                        nabla = currCost - cost
                        nabla_arg = set(result)
                    result.add(drop)
        if len(result) < len(homes):
            setminus = total.difference(result)
            for toAdd in setminus:
                result.add(toAdd)
                _, cost = getTSPfast(shortest_path, result, starting_location, homes)
                if (currCost - cost > nabla):
                    nabla = currCost - cost
                    nabla_arg = set(result)
                result.remove(toAdd)
        if (nabla == 0):
            break;
        else:
            result = nabla_arg
        counter += 1
    return result

def runDescent12Mix(homes, starting_location, shortest_path, initial_set, num_iterations):
    """
    Run Descent12Mix algorithm on the given set of drop off locations.
    Descent12Mix runs Descent1 algorithm and runs an iteration of Descent2 afterward.
    It terminates if Descent2 does not find a better move and re-loop if it finds one.
    An iteration runs in O(n^2) * O(TSP) but is expected to perform faster than Descent2.
    """
    result = set(initial_set)
    counter = 0
    total = set(range(0, len(shortest_path)))
    while (counter < num_iterations):
        _, currCost = getTSPfast(shortest_path, result, starting_location, homes)
        nabla = 0
        nabla_arg = set()
        if (len(result) > 1):
            for drop in list(result):
                result.remove(drop)
                _, cost = getTSPfast(shortest_path, result, starting_location, homes)
                if (currCost - cost > nabla):
                    nabla = currCost - cost
                    nabla_arg = set(result)
                result.add(drop)
        if len(result) < len(homes):
            setminus = total.difference(result)
            for toAdd in setminus:
                result.add(toAdd)
                _, cost = getTSPfast(shortest_path, result, starting_location, homes)
                if (currCost - cost > nabla):
                    nabla = currCost - cost
                    nabla_arg = set(result)
                result.remove(toAdd)
        if (nabla == 0):
            break;
        else:
            result = nabla_arg
        counter += 1
    nabla = 0
    nabla_arg = set()
    _, currCost = getTSPfast(shortest_path, result, starting_location, homes)
    for drop in list(result): # Descent2
        result.remove(drop)
        setminus = total.difference(result)
        for toAdd in setminus:
            if (drop != toAdd):
                result.add(toAdd)
                _, cost = getTSPfast(shortest_path, result, starting_location, homes)
                if (currCost - cost > nabla):
                    nabla = currCost - cost
                    nabla_arg = set(result)
                result.remove(toAdd)
                result.add(drop)
    if (nabla != 0):
        a = runDescent12Mix(homes, starting_location, shortest_path, nabla_arg, num_iterations)
        return a
    return result

def runDescent2(homes, starting_location, shortest_path, initial_set, num_iterations):
    """
    Run Descent2 algorithm on the given set of drop off locations.
    Descent2 is similar to Descent1 but it also checks whether switching a drop off location
    with a non-drop off location produce a better running time.
    An iteration runs in O(n^2) * O(TSP).
    """
    result = set(initial_set)
    counter = 0
    total = set(range(0, len(shortest_path)))
    while (counter < num_iterations):
        _, currCost = getTSPfast(shortest_path, result, starting_location, homes)
        nabla = 0
        nabla_arg = set()
        if (len(result) > 1):
            for drop in list(result):
                result.remove(drop)
                _, cost = getTSPfast(shortest_path, result, starting_location, homes)
                if (currCost - cost > nabla):
                    nabla = currCost - cost
                    nabla_arg = set(result)
                result.add(drop)
        for drop in list(result): # Descent2
            result.remove(drop)
            setminus = total.difference(result)
            for toAdd in setminus:
                if (drop != toAdd):
                    result.add(toAdd)
                    _, cost = getTSPfast(shortest_path, result, starting_location, homes)
                    if (currCost - cost > nabla):
                        nabla = currCost - cost
                        nabla_arg = set(result)
                    result.remove(toAdd)
                    result.add(drop)
        if len(result) < len(homes):
            setminus = total.difference(result)
            for toAdd in setminus:
                result.add(toAdd)
                _, cost = getTSPfast(shortest_path, result, starting_location, homes)
                if (currCost - cost > nabla):
                    nabla = currCost - cost
                    nabla_arg = set(result)
                result.remove(toAdd)
        if (nabla == 0):
            break;
        else:
            result = nabla_arg
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
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

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
