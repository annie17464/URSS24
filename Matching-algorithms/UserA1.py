# we will use networkx to solve our problem 
import networkx as nx

# since we are using user inputs, we want to make sure the inputted matching is a valid matching. 
# we define a function is_viable_matching: 
def is_viable_matching(graph, matching):
    matched_nodes = set()
    
    for x, y in matching:
        # Check if (x, y) is a valid edge in the graph
        if not graph.has_edge(x, y):
            return False
        
        # Check if either node is already matched
        if x in matched_nodes or y in matched_nodes:
            return False
        
        # Add the nodes to the set of matched nodes
        matched_nodes.add(x)
        matched_nodes.add(y)
    
    return True

def print_matching(matching, X):
    # we format matching pairs 
    for x, y in matching:
        if x in X:
            print(f"{x} -- {y}")

def main():
    # Input nodes in set X
    X = input("Enter the nodes in set X separated by spaces: ").split()
    
    # Input nodes in set Y
    Y = input("Enter the nodes in set Y separated by spaces: ").split()
    
    # Input edges between X and Y
    edges_input = input("Please enter edges in the form (x,y) separated by spaces: ")
    edges = [tuple(edge.strip('()').split(',')) for edge in edges_input.split()]
    
    # Input initial matching
    initial_matching_input = input("Please enter your initial matching in the form (x,y) separated by spaces: ")
    initial_matching = [tuple(match.strip('()').split(',')) for match in initial_matching_input.split()]
    
    # Create a bipartite graph
    G = nx.Graph()
    G.add_nodes_from(X, bipartite=0)
    G.add_nodes_from(Y, bipartite=1)
    G.add_edges_from(edges)
    
    # we validate the initial matching
    if not is_viable_matching(G, initial_matching):
        print("Your initial matching is not viable, but we can directly find the maximum matching:")
    else:
        for x, y in initial_matching:
            if G.has_edge(x, y):
                G[x][y]['matched'] = True
    
    # we make sure the graph is connected and bipartite 
    if not nx.is_bipartite(G):
        print("The graph is not bipartite.")
        return
    
    # we find the maximum matching using NetworkX
    max_matching_dict = nx.bipartite.maximum_matching(G, X)
    
    # Convert dictionary to list of tuples
    max_matching = [(x,y) for x, y in max_matching_dict.items() if x in X]
    
    # we compare the initial matching with our maximum matching
    if set(initial_matching) == set(max_matching):
        print("The initial matching is the maximum matching!")
        print_matching(initial_matching, X)
    elif not is_viable_matching(G, initial_matching):
        print_matching(max_matching, X) 
    else:
        print("Augmenting path found! The maximum matching is")
        print_matching(max_matching, X)

if __name__ == "__main__":
    main()
