import matplotlib.pyplot as plt
import networkx as nx

def create_architecture_diagram():
    G = nx.DiGraph()

    pos = {
        "User": (0, 2),
        "Streamlit\nFrontend": (2, 2),
        "LLM Chatbot": (4, 2),
        "Snowflake": (2, 0),
        "TPC-DS\nDataset": (4, 0)
    }

    for node, position in pos.items():
        G.add_node(node, pos=position)

    edges = [
        ("User", "Streamlit\nFrontend", "1. Interacts with"),
        ("Streamlit\nFrontend", "Snowflake", "2a. Sends SQL queries"),
        ("Streamlit\nFrontend", "LLM Chatbot", "2b. Sends natural\nlanguage queries"),
        ("LLM Chatbot", "Snowflake", "3. Generates SQL"),
        ("Snowflake", "Streamlit\nFrontend", "4. Returns results"),
        ("Streamlit\nFrontend", "User", "5. Displays results"),
        ("TPC-DS\nDataset", "Snowflake", "Loaded into")
    ]
    G.add_edges_from((u, v) for u, v, _ in edges)

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=4000, alpha=0.8)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

    curved_edges = [
        ("User", "Streamlit\nFrontend"),
        ("Streamlit\nFrontend", "User"),
        ("Streamlit\nFrontend", "Snowflake"),
        ("Snowflake", "Streamlit\nFrontend")
    ]
    straight_edges = [edge for edge in G.edges() if edge not in curved_edges]
    
    nx.draw_networkx_edges(G, pos, edgelist=straight_edges, edge_color='gray', arrows=True, arrowsize=20)
    arc_rad = 0.25
    nx.draw_networkx_edges(G, pos, edgelist=curved_edges, edge_color='gray', arrows=True, arrowsize=20, connectionstyle=f'arc3,rad={arc_rad}')

    edge_labels = {(u, v): label for u, v, label in edges}
    curved_edge_labels = {}
    for edge in curved_edges:
        if edge in edge_labels:
            curved_edge_labels[edge] = edge_labels[edge]
            del edge_labels[edge]
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=curved_edge_labels, font_size=8, label_pos=0.3)

    plt.title("Marketing Analytics Tool Architecture", fontsize=16, fontweight="bold")
    plt.axis('off')
    plt.savefig("marketing_analytics_tool_architecture.png", dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    create_architecture_diagram()