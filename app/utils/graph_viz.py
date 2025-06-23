import networkx as nx
import colorsys
import tempfile
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def generate_contrast_colors(n):
    colors = []
    for i in range(n):
        hue = i / n
        saturation = 1.0
        value = 1.0
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        colors.append(rgb)
    return colors

def generate_color_map(node_types):
    colors = generate_contrast_colors(len(node_types))
    return dict(zip(node_types, colors))

def draw_kg_image(nodes, edges):
    G = nx.DiGraph()
    for node_id, node_type in nodes:
        G.add_node(node_id, type=node_type)
    for source, target, rel_type in edges:
        G.add_edge(source, target, label=rel_type)

    pos = nx.spring_layout(G, seed=42)
    node_colors = []
    color_map = generate_color_map([node[1]['type'] for node in G.nodes(data=True)])
    
    for node in G.nodes(data=True):
        node_type = node[1]['type']
        node_colors.append(color_map.get(node_type, 'gray'))

    plt.figure(figsize=(12, 9))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->', width=2)

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=9)

    legend_elements = [Patch(facecolor=color, label=type_) for type_, color in color_map.items()]

    img_path = tempfile.mktemp(suffix=".png")
    plt.title("Knowledge Graph", fontsize=15)
    plt.axis('off')
    plt.tight_layout()
    plt.legend(handles=legend_elements, title="Node Types")
    plt.savefig(img_path)
    plt.close()

    return img_path
