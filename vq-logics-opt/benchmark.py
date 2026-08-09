import networkx as nx
import numpy as np
import time
import torch
from sb_solver import SimulatedBifurcationSolver
from maxcut import solve_maxcut

def greedy_maxcut(G):
    """Simple greedy heuristic for Max-Cut."""
    cut_set = set()
    non_cut_set = set(G.nodes)
    
    # Randomly initialize one node
    start_node = list(G.nodes)[0]
    cut_set.add(start_node)
    non_cut_set.remove(start_node)
    
    improved = True
    while improved:
        improved = False
        for node in list(non_cut_set):
            # Calculate gain if moved to cut_set
            gain = 0
            for neighbor in G.neighbors(node):
                if neighbor in non_cut_set:
                    gain += 1
                elif neighbor in cut_set:
                    gain -= 1
            if gain > 0:
                cut_set.add(node)
                non_cut_set.remove(node)
                improved = True
                
        for node in list(cut_set):
            # Calculate gain if moved to non_cut_set
            gain = 0
            for neighbor in G.neighbors(node):
                if neighbor in cut_set:
                    gain += 1
                elif neighbor in non_cut_set:
                    gain -= 1
            if gain > 0:
                non_cut_set.add(node)
                cut_set.remove(node)
                improved = True

    # Calculate final cut size
    cut_size = 0
    for u, v in G.edges:
        if (u in cut_set and v in non_cut_set) or (v in cut_set and u in non_cut_set):
            cut_size += 1
            
    return cut_size

def run_benchmarks():
    sizes = [100, 500, 1000]
    p = 0.5
    
    print(f"{'Graph Size':<15} | {'Greedy Cut':<15} | {'Greedy Time':<15} | {'SB Cut':<15} | {'SB Time':<15}")
    print("-" * 80)
    
    for n in sizes:
        G = nx.erdos_renyi_graph(n, p, seed=42)
        
        # Benchmark Greedy
        start_time = time.time()
        greedy_cut = greedy_maxcut(G)
        greedy_time = time.time() - start_time
        
        # Benchmark SB
        start_time = time.time()
        # For larger graphs, reduce batch size and steps to keep time reasonable for this test
        batch_size = 32 if n <= 500 else 8
        steps = 300 if n <= 500 else 150
        _, sb_cut = solve_maxcut(G, batch_size=batch_size, steps=steps, verbose=False)
        sb_time = time.time() - start_time
        
        print(f"{n:<15} | {greedy_cut:<15} | {greedy_time:<15.4f} | {sb_cut:<15} | {sb_time:<15.4f}")

if __name__ == "__main__":
    run_benchmarks()
