"""Build graph from edges data"""

from data_structures import AdjacencyListGraph
from data_loader import load_edges

def build_friendship_graph():
    """
    Build adjacency list graph from edges file.
    Returns: AdjacencyListGraph object
    """
    
    print("\n🔨 Building friendship graph...")
    
    edges_df = load_edges()
    graph = AdjacencyListGraph()
    
    print("   Adding edges to graph...")
    
    for idx, row in edges_df.iterrows():
        graph.add_edge(row['u'], row['v'])
        
        if (idx + 1) % 100000 == 0:
            print(f"   Processed {idx+1:,} edges...")
    
    print(f"\n✓ Graph built successfully!")
    print(f"   Nodes (users): {graph.num_nodes():,}")
    print(f"   Edges (friendships): {graph.num_edges_count():,}")
    
    avg_degree = graph.num_edges_count() / graph.num_nodes() if graph.num_nodes() > 0 else 0
    print(f"   Average friends per user: {avg_degree:.1f}")
    
    return graph


print("✓ Graph builder module ready")
