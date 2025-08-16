import networkx as nx
import matplotlib.pyplot as plt

def visualize_mesh(connections):
    """
    connections: list of tuples (node1, node2)
    """
    G = nx.Graph()
    G.add_edges_from(connections)

    plt.figure(figsize=(6,6))
    nx.draw(G, with_labels=True, node_size=2000, node_color="skyblue", font_size=10)
    plt.title("NeuroWeave Mesh")
    plt.show()
  
