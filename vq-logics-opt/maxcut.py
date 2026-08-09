import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from sb_solver import SimulatedBifurcationSolver

def generate_random_graph(n, p=0.5):
    """Generate an Erdos-Renyi random graph."""
    return nx.erdos_renyi_graph(n, p)

def solve_maxcut(graph, batch_size=10, steps=1000, verbose=True):
    """
    Solves the Max-Cut problem on the given graph using Simulated Bifurcation.
    """
    n = len(graph.nodes)
    
    # Adjacency matrix (W)
    W = nx.to_numpy_array(graph)
    
    # For Max-Cut, we want to maximize sum W_ij (1 - s_i s_j) / 2
    # This is equivalent to minimizing sum W_ij s_i s_j
    # So our Ising interaction matrix J is just -W
    J = -W
    
    if verbose:
        print(f"Solving Max-Cut for graph with {n} nodes and {len(graph.edges)} edges...")
    
    solver = SimulatedBifurcationSolver(dt=0.1, steps=steps, device='cpu')
    best_spins, best_energy = solver.solve_ising(J, batch_size=batch_size)
    
    # Calculate actual cut value
    # E_ising = -0.5 * sum J_ij s_i s_j = 0.5 * sum W_ij s_i s_j
    # Cut = 0.25 * sum W_ij (1 - s_i s_j)
    # Since sum W_ij = 2 * num_edges (for unweighted)
    # Cut = 0.5 * num_edges - 0.5 * E_ising
    
    # Direct calculation of cut size
    cut_size = 0
    for u, v in graph.edges:
        # If spins are different (one is +1, other is -1), product is -1
        if best_spins[u] * best_spins[v] < 0:
            cut_size += 1
            
    if verbose:
        print(f"Best Ising Energy found: {best_energy:.4f}")
        print(f"Resulting Cut Size: {cut_size}")
    
    return best_spins, cut_size

if __name__ == "__main__":
    # Test with a small graph
    G = generate_random_graph(50, p=0.3)
    spins, cut_size = solve_maxcut(G, batch_size=64, steps=500)
    
    # Plotting (saved to file)
    color_map = ['red' if s > 0 else 'blue' for s in spins]
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, node_color=color_map, with_labels=False, node_size=50)
    plt.title(f"Max-Cut Solution (Cut Size: {cut_size})")
    plt.savefig("maxcut_result.png")
    print("Graph visualization saved to maxcut_result.png")
