import networkx as nx
import re
import matplotlib.pyplot as plt
import random
import math
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom


# Veralteter Versuch mit pypot! 

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
            if ".." in node_name:
                continue
            # Add the node to the graph
            graph.add_node(node_name, size=node_size)

            # Add the edges to other nodes
            destination_list = []
            for edge in edges:
                destination_list.append(edge)
        except:

            print("Error " + line)

    # --------------------create Edge list

    # top_level_edge_list = create_top_level_edge_list(graph)
    top_level_edge_list = read_tuples_from_file("top_level_edge_list.txt")
    print(top_level_edge_list)
    print("top_level_edge_list ist erstellt")

    # --------------------create Nodes list
    # top_level_node_list = create_top_level_node_list(graph)
    top_level_node_list = read_tuples_from_file("top_level_node_list.txt")
    print(top_level_node_list)
    print("top_level_node_list ist erstellt und die graph Erstellung beginnt")

    graph2 = nx.Graph()
    counter = 0
    for node in top_level_node_list:
        if int(node[1]) > 100:
            color = random.choice(
                ['red', 'green', 'blue', 'yellow', 'purple', 'orange'])
            alpha = 0.5
            node_color = color
            graph2.add_node(node[0], size=math.sqrt(node[1]), color=node_color)
        else:
            counter += 1
    graph2.add_node("Rest", color='gray')

    for edge in top_level_edge_list:
        if edge[2] > 50:
            graph2.add_edge(edge[0], edge[1], weight=edge[2])
        else:
            graph2.add_edge(edge[0], "Rest", weight=counter)
    write_gexf_file(graph2, "gexf_top_level.txt")
    draw_graph2(top_level_node_list, top_level_edge_list)
    # write_gexf_file(graph, "full.gexf")

#


def write_gexf_file(graph, file_path):
    # Create the GEXF root element
    root = ET.Element("gexf", version="1.3",
                      xmlns="http://www.gexf.net/1.3draft")
    graph_element = ET.SubElement(
        root, "graph", mode="static", defaultedgetype="directed")

    # Create the nodes element and add nodes to it
    nodes_element = ET.SubElement(graph_element, "nodes")
    for node, attributes in graph.nodes(data=True):
        node_element = ET.SubElement(
            nodes_element, "node", id=str(node), label=str(node))
        for attr_key, attr_value in attributes.items():
            ET.SubElement(node_element, "attvalues").append(
                ET.Element("attvalue", {"for": attr_key,
                           "value": str(attr_value)})
            )

    # Create the edges element and add edges to it
    edges_element = ET.SubElement(graph_element, "edges")
    for u, v, attributes in graph.edges(data=True):
        # Convert attribute values to strings
        attr_dict = {attr_key: str(attr_value)
                     for attr_key, attr_value in attributes.items()}
        ET.SubElement(edges_element, "edge", source=str(u),
                      target=str(v), **attr_dict)

    # Create the XML tree and write it to a file
    xml_tree = ET.ElementTree(root)
    xml_tree.write(file_path, encoding="utf-8", xml_declaration=True)

    # Format the XML file to be more readable
    xml_string = minidom.parseString(
        ET.tostring(root)).toprettyxml(indent="  ")
    with open(file_path, "w") as file:
        file.write(xml_string)


def read_tuples_from_file(file_path):
    tuples_list = []

    try:
        with open(file_path, 'r') as file:
            for line in file:

                line = line.strip()
                if line:  # Skip empty lines
                    # Split the line by space and convert each element to a tuple
                    try:
                        line = line.replace(", ", ",")
                        parsed_tuple = list(line.split(" "))
                        tuples_list.append(parsed_tuple)

                    except ValueError:
                        print(f"Invalid tuple format: {line}")

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    result = []
    for elem in tuples_list[0]:
        result.append(eval(elem))
    return result


def create_top_level_edge_list(graph):
    top_level_edge_list = []
    top_level_edge_list_long = []
    visited_list_edges = []
    for edge in graph.edges:
        top_level_edge_list_long.append(
            (edge[0].split("/")[0], edge[1].split("/")[0]))

    for edge in top_level_edge_list_long:
        if edge in visited_list_edges:
            continue
        top_level_edge_list.append(
            (edge[0], edge[1], top_level_edge_list_long.count(edge)))
        visited_list_edges.append(edge)

    with open('top_level_edge_list.txt', 'w') as top_level_edge_list_txt:
        for edge in top_level_edge_list:
            top_level_edge_list_txt.write(str(edge)+";")
    return top_level_edge_list


def create_top_level_node_list(graph):
    top_level_node_list = []
    top_level_node_list_long = []
    visited_list_node = []
    for node in graph.nodes:
        top_level_node_list_long.append(
            node.split("/")[0])
    for node in top_level_node_list_long:
        if node in visited_list_node:
            continue
        top_level_node_list.append(
            (node, top_level_node_list_long.count(node)))
        visited_list_node.append(node)

    with open('top_level_node_list.txt', 'w') as top_level_node_list_txt:
        for node in top_level_node_list:
            top_level_node_list_txt.write(str(node)+";")
    return top_level_node_list


def draw_graph(node_list, edge_list):
    graph = nx.Graph()
    counter = 0
    test = node_list[0]
    for node in node_list:
        if int(node[1]) > 100:
            color = random.choice(
                ['red', 'green', 'blue', 'yellow', 'purple', 'orange'])
            alpha = 0.5
            node_color = color
            graph.add_node(node[0], size=math.sqrt(node[1]), color=node_color)
        else:
            counter += 1

    # Add the 'Rest' node without the 'size' attribute
    graph.add_node("Rest", color='gray')

    for edge in edge_list:
        if edge[2] > 50:
            graph.add_edge(edge[0], edge[1], weight=edge[2])

    # Draw the network graph
    plt.figure(figsize=(25, 35))
    pos = nx.spring_layout(graph, k=0.5, iterations=100, scale=1)
    node_sizes = [graph.nodes[node].get(
        'size', 1) * 100 for node in graph.nodes]
    # node_colors = [graph.nodes[node] for node in graph.nodes]
    nx.draw_networkx_nodes(graph, pos, node_color=random.choice(
        ['red', 'green', 'blue', 'yellow', 'purple', 'orange']),
        node_size=node_sizes, alpha=0.5)
    nx.draw_networkx_edges(graph, pos, edge_color='gray', alpha=0.7)
    nx.draw_networkx_labels(graph, pos, font_color='black')
    plt.title('Network Graph of the Linux Kernel')
    plt.axis('off')
    plt.show()
    return graph


if __name__ == "__main__":
    main()


# Print the graph information
# print('Nodes:', graph.number_of_nodes())
# print('Edges:', graph.number_of_edges())

# Access node attributes
# for node in graph:
#    print('Node:', node)

# print(graph.nodes, graph.size, graph.edges,)
# Access edge information
# for edge in graph.edges:
#    print('Edge:', edge)


# Draw nodes and edges
# nx.draw(graph, pos, with_labels=True, node_size=node_sizes)
# plt.title('Network Graph')  # Set the title of the graph
# plt.show()  # Display the graph
