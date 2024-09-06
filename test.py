import matplotlib.pyplot as plt
import networkx as nx

def create_flowchart():
    # Create a directed graph
    G = nx.DiGraph()

    # Adding nodes
    nodes = ["Start", "Init", "Read Data", "Display Menu", "User Choice",
             "Decision", "Add Participant", "Sort Surname", "Sort Place",
             "Display Younger", "Exit Program", "Invalid Choice", "Close File", "End"]
    G.add_nodes_from(nodes)

    # Adding edges
    edges = [
        ("Start", "Init"), ("Init", "Read Data"), ("Read Data", "Display Menu"),
        ("Display Menu", "User Choice"), ("User Choice", "Decision"),
        ("Decision", "Add Participant", {'label': 'Choice == 1'}),
        ("Decision", "Sort Surname", {'label': 'Choice == 2'}),
        ("Decision", "Sort Place", {'label': 'Choice == 3'}),
        ("Decision", "Display Younger", {'label': 'Choice == 4'}),
        ("Decision", "Exit Program", {'label': 'Choice == 5'}),
        ("Decision", "Invalid Choice", {'label': 'Invalid'}),
        ("Add Participant", "Close File"), ("Sort Surname", "Close File"),
        ("Sort Place", "Close File"), ("Display Younger", "Close File"),
        ("Exit Program", "Close File"), ("Invalid Choice", "Display Menu"),
        ("Close File", "End")
    ]
    G.add_edges_from(edges)

    # Define node positions in a dictionary
    pos = nx.shell_layout(G)  # This layout places nodes in concentric circles

    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=4000, edge_color='k', linewidths=1, font_size=10, font_color='black')

    # Draw edge labels
    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True) if 'label' in d}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Show plot
    plt.show()

create_flowchart()
