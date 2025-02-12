import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz

# Load your CSV file
df = pd.read_csv("/Users/hadibhidya/Desktop/PragerU-Project/famous_names_by_channel_w_gender_and_race_2024-11-11_12-40-29.csv")

# Define similarity threshold
SIMILARITY_THRESHOLD = 95

# Group data by channel
for channel, group in df.groupby("Channel"):
    # Create a graph for each channel
    G = nx.Graph()

    # Add nodes (each name in the current channel group)
    for idx, row in group.iterrows():
        G.add_node(row['Name'], count=row['Count'])

    # Calculate pairwise similarity and add edges within the channel group
    for i, row1 in group.iterrows():
        for j, row2 in group.iterrows():
            if i < j:
                similarity = fuzz.ratio(row1['Name'], row2['Name'])
                if similarity > SIMILARITY_THRESHOLD:
                    G.add_edge(row1['Name'], row2['Name'], weight=similarity)

    # Draw the graph for the current channel
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, seed=42)

    # Draw nodes with size proportional to their 'Count' value
    node_sizes = [G.nodes[node]['count'] * 20 for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="skyblue", edgecolors="black")

    # Draw edges with width proportional to the similarity score
    edge_weights = [G[u][v]['weight'] / 10 for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5, edge_color="gray")

    # Draw labels for nodes
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    # Add a title indicating the channel and display the plot
    plt.title(f"Name Similarity Graph - Channel: {channel}")
    plt.show()
