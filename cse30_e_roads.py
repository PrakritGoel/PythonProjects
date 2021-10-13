"""
Implement a weighted directed graph. Use Dijkstra's shortest path
algorithm to find the shortest distance between two European cities.
If a path does not exist, between the two given cities, the
program says so.

Sample Output
$ python3 cse30_e_roads.py "Nizhny Novgorod" Munich
Nizhny Novgorod
Vladimir
Moscow
Velikiye Luki
Rēzekne
Daugavpils
Ukmergė
Kaunas
Warsaw
Piotrków Trybunalski
Wrocław
Legnica
Jelenia Góra
Harrachov
Železný Brod
Turnov
Mladá Boleslav
Prague
Plzeň
Bayerisch Eisenstein
Deggendorf
Munich

$ python3 cse30_e_roads.py Munich London
No path exists between Munich and London

The graph is constructed based on three files
vertex_names.txt: Contains the names of the European cities
network.txt: Contains the connections between the cities
vertex_locations.txt: Contains the latitude and longitude information
                      for the cities

The first two files are used to create the vertices and edges of the graph.
The information about the latitude and longitude is used to determine the
distance between cities, which gives the weight to the edges of the graph.
"""
from __future__ import print_function

from collections import defaultdict
import math
import sys


class Graph(defaultdict):
    """
    The Graph class creates a defaultdict of a dictionary object to
    implement a weight directed graph.
    """

    def __init__(self):
        """
        Initialize the Graph as a defaultdict of dict
        """
        super().__init__(dict)

    def vertices(self):
        """
        Return all the vertices of the graph
        return: Set of vertices
        """
        g_vertices = set()
        for keys, values in self.items():
            g_vertices.add(keys)
            for vertices in values.keys():
                g_vertices.add(vertices)

        return g_vertices

    def edges(self):
        """
        Find all the edges in the graph
        return: The set of edges
        """
        edges_set = set()
        for from_vertex, values in self.items():
            for to_vertex, edge_weight in values.items():
                edge = (from_vertex, to_vertex, edge_weight)
                edges_set.add(edge)

        return edges_set

    def neighbors(self, vertex):
        """
        Set of all vertices for which a path exists from the given vertex
        param vertex: Vertex of interest
        return: Set of vertices adjacent to the input vertex
        """
        return set(self[vertex].keys())


def haversine(pos1, pos2):
    """
    Given the latitude and longitude of two places, this function calculates the distance
    on the surface of the earth between them. The details of the algorithm are available at
    https://en.wikipedia.org/wiki/Haversine_formula
    param pos1: tuple containing latitude and longitude of the first location
    param pos2: tuple containing latitude and longitude of the second location
    return: The distance between the two points
    """
    lat1, lon1 = pos1
    lat2, lon2 = pos2
    # r = 6371e3  # metres
    phi1 = lat1 * math.pi / 180  # phi, lambda in radians
    phi2 = lat2 * math.pi / 180
    delta_phi = (lat2 - lat1) * math.pi / 180
    delta_lambda = (lon2 - lon1) * math.pi / 180

    a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + math.cos(phi1) * \
        math.cos(phi2) * math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    d = 6371e3 * c  # in metres
    return d


def shortest_path(g: Graph, node_1: str, node_2: str, num_args):
    """
    Implement Dijsktra's shortest path algorithm.
    param g: Graph formed from the data provided
    param node_1: Start node
    param node_2: Destination Node
    return: None
    """
    visited = set()
    unvisited = g.vertices()

    vertex_weights = dict()
    for node in unvisited:
        vertex_weights[node] = float('inf')

    unvisited_vertex_weights = vertex_weights.copy()
    vertex_weights[node_1] = 0

    previous_vertex = {node_1: node_1}
    current_node = node_1

    while unvisited != ():
        neighbors = list(g.neighbors(current_node) - visited)

        for next_node in neighbors:
            new_vertex_weight = g[current_node][next_node] + vertex_weights[current_node]
            if new_vertex_weight < vertex_weights[next_node]:
                vertex_weights[next_node] = new_vertex_weight
                unvisited_vertex_weights[next_node] = new_vertex_weight
                previous_vertex[next_node] = current_node

        unvisited.remove(current_node)
        visited.add(current_node)
        del unvisited_vertex_weights[current_node]

        # To get the next node, we must find the unvisited node with the lowest weight.
        # This information is being maintained in the unvisited_vertex_weights dictionary.
        # Sort this by value and pick the 0th element for the next node
        current_node = ([k for k, v in sorted(unvisited_vertex_weights.items(),
                                              key=lambda item: item[1])])[0]

        if current_node == node_2:
            if node_2 not in previous_vertex.keys():
                print('No path exists between', node_1, 'and', node_2, file=sys.stderr)
                sys.exit(1)
            break

    if unvisited == ():
        print('No path exists between', node_1, 'and', node_2, file=sys.stderr)
        sys.exit(1)

    # Create the path by going through the table of previous vertices
    previous_node = node_2
    reversed_path = [node_2]

    while previous_node != node_1:
        reversed_path.append(previous_vertex[previous_node])
        previous_node = previous_vertex[previous_node]

    if num_args == 2:
        for i in list(reversed(reversed_path)):
            print(i)
    else:
        # Construct a URL giving latitudes and longitudes of the cities

        my_url = 'https://www.google.com/maps/dir/'
        for i in list(reversed(reversed_path)):
            (lat, lon) = city_location[i]
            my_url += '{:0.3f}'.format(lat) + ',' + '{:0.3f}'.format(lon) + '/'
        print(my_url)


if __name__ == '__main__':
    # Create a list of all the cities
    city_list = [None]
    with open('/srv/datasets/e-roads/vertex_names.txt', 'r') as fh:
        cities = fh.readlines()

    for city in cities:
        city = city.rstrip()
        index, city_name = city.split('\t')
        city_list.append(city_name)

    # Read the latitudes and longitudes for each city, save it as a tuple.
    # Create a dictionary, with the name as key, and the tuple as value.
    with open('/srv/datasets/e-roads/vertex_locations.txt', 'r') as fh:
        locations = fh.readlines()

    city_location = dict()
    for line in locations:
        line = line.rstrip()
        idx, latitude, longitude = line.split(' ')
        idx = int(idx)
        latitude = float(latitude)
        longitude = float(longitude)
        coordinate = (latitude, longitude)
        city_location[city_list[idx]] = coordinate

    # Find all the cities connected to each other, and make a graph for them.
    with open('/srv/datasets/e-roads/network.txt', 'r') as fh:
        edges = fh.readlines()

    city_network_graph = Graph()
    for entry in edges:
        entry = entry.rstrip()
        city_idx_1 = int(entry.split(' ')[0])
        city_idx_2 = int(entry.split(' ')[1])
        city_1 = city_list[city_idx_1]
        city_2 = city_list[city_idx_2]

        # Get the latitudes and longitudes for the two cities
        city_1_pos = city_location[city_1]
        city_2_pos = city_location[city_2]

        # Calculate the distance between them using the haversine formula
        distance = haversine(city_1_pos, city_2_pos)

        # Assign the distance between them as a weight for their edge
        city_network_graph[city_1][city_2] = distance
        city_network_graph[city_2][city_1] = distance

    city_1 = sys.argv[1]
    city_2 = sys.argv[2]

    if city_1 not in city_list:
        print(city_1, 'is not a connected city in Europe', file=sys.stderr)
        sys.exit(1)

    if city_2 not in city_list:
        print(city_2, 'is not a connected city in Europe', file=sys.stderr)
        sys.exit(1)

    if city_1 == city_2:
        if len(sys.argv) == 3:
            print(city_1)
        else:
            URL = 'https://www.google.com/maps/dir/'
            (latitude, longitude) = city_location[city_1]
            URL += '{:0.3f}'.format(latitude) + ',' + '{:0.3f}'.format(longitude) + '/'
            print(URL)
    else:
        shortest_path(city_network_graph, city_1, city_2, len(sys.argv) - 1)
