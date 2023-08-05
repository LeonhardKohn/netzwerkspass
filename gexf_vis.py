import networkx as nx
import re
import matplotlib.pyplot as plt
import random
import math
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import Counter


def count_destinations(graph):
    """
    Function to count the occurrences of destination nodes in a graph.

    Parameters:
    graph (nx.Graph): The NetworkX graph to analyze.

    Returns:
    list: A list of tuples where each tuple contains a node and its count.
    """
    destinations = [edge[1] for edge in graph.edges()]
    counts = Counter(destinations)
    return [(node, count) for node, count in counts.items()]


def remove_isolates(graph):
    """
    Function to remove isolated nodes (i.e., nodes with no edges) from a graph.

    Parameters:
    graph (nx.Graph): The NetworkX graph to analyze.
    """
    isolates = list(nx.isolates(graph))
    graph.remove_nodes_from(isolates)
    return graph


def remove_less_connected(graph, min_edges=20):
    """
    Function to remove edges from a graph if the destination node has less than min_edges incoming edges.

    Parameters:
    graph (nx.Graph): The NetworkX graph to analyze.
    min_edges (int): The minimum number of incoming edges a node should have.
    """
    # Get a list of nodes and their counts
    node_counts = count_destinations(graph)

    # Find nodes with less than min_edges incoming edges
    less_connected_nodes = [node for node,
                            count in node_counts if count < min_edges]

    # Create a copy of the graph so we can modify it while iterating
    graph_copy = graph.copy()

    # Iterate over the edges of the copy of the graph
    for edge in graph_copy.edges():
        # If the destination node of the edge is in less_connected_nodes, remove the edge from the original graph
        if edge[1] in less_connected_nodes:
            graph.remove_edge(*edge)

    return graph


def main():
    sys.setrecursionlimit(10**6)
    # Read the include_list.txt file
    with open('include_list.txt', 'r') as file:
        lines = file.readlines()

    # Create an empty network graph
    graph = nx.Graph()

    # Process each line and add nodes and edges to the graph

    for line in lines:
        if re.search("None", line):
            line = line.replace("None ", "")
        try:
            parts = line.strip().split(' ')
            node_name = parts[0]
            edges = parts[1:-1]
            node_size = int(parts[-1])
        except:
            print("Error "+line)
            continue
        if ".." in node_name:
            continue

        # Add the node to the graph
        if node_size < 20:
            continue

        graph.add_node(node_name, size=node_size)

        # Add the edges to other nodes
        destination_list = []
        for edge in edges:
            graph.add_edge(node_name, edge)

        # Alle edges und nodes sind hinzu gefügt.

    # try to write all edges in a list. at the end should be the number of occurrences

    graph = remove_less_connected(graph)
    graph = remove_isolates(graph)
    nx.write_gexf(graph, "linux_kernel.gexf")


if __name__ == "__main__":
    main()
