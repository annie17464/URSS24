import networkx as nx

# Create a bipartite graph
B = nx.Graph()

# Add nodes with the node attribute "bipartite"
X = ['x1', 'x2', 'x3']
Y = ['y1', 'y2', 'y3']
B.add_nodes_from(X, bipartite=0)
B.add_nodes_from(Y, bipartite=1)

# Add edges
edges = [
    ('x1', 'y1'),
    ('x1', 'y2'),
    ('x2', 'y1'),
    ('x3', 'y2'),
    ('x3', 'y3')
]
B.add_edges_from(edges)

# We can define an initial matching:
initial_matching = {
    'x1': 'y2',
    'y2': 'x1',
    'x2': 'y1',
    'y1': 'x2'
}

# Update the graph with the initial matching
for x, y in initial_matching.items():
    if B.has_edge(x, y):
        B[x][y]['matched'] = True

# Formatting the matching: 
def print_matching(matching):
    pairs = [(x, y) for x, y in matching.items() if x in X]
    for x, y in pairs:
        print(f"{x} -- {y}")

# Find a maximum matching
matching = nx.bipartite.maximum_matching(B)

print("Maximum Matching:")
print_matching(matching)