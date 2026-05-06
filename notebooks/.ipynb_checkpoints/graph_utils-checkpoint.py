import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import random

def convert_graphrag_format(graph_data):
    """Convert GraphRAG relationship list to ECharts format"""
    nodes_dict = {}
    links = []
    
    # Extract nodes and relationships from the list
    for item in graph_data:
        if not isinstance(item, dict):
            continue
            
        start_node = item.get("start_node", {})
        end_node = item.get("end_node", {})
        relation = item.get("relation", "related_to")
        
        # Process start node
        start_id = ""
        end_id = ""
        if start_node:
            start_id = start_node.get("properties", {}).get("name", "")
            if start_id and start_id not in nodes_dict:
                nodes_dict[start_id] = {
                    "id": start_id,
                    "name": start_id[:30],
                    "category": start_node.get("properties", {}).get("schema_type", start_node.get("label", "entity")),
                    "symbolSize": 25,
                    "properties": start_node.get("properties", {})
                }
        
        # Process end node
        if end_node:
            end_id = end_node.get("properties", {}).get("name", "")
            if end_id and end_id not in nodes_dict:
                nodes_dict[end_id] = {
                    "id": end_id,
                    "name": end_id[:30],
                    "category": end_node.get("properties", {}).get("schema_type", end_node.get("label", "entity")),
                    "symbolSize": 25,
                    "properties": end_node.get("properties", {})
                }
        
        # Add relationship
        if start_id and end_id:
            links.append({
                "source": start_id,
                "target": end_id,
                "name": relation,
                "value": 1
            })
    
    # Create categories
    categories_set = set()
    for node in nodes_dict.values():
        categories_set.add(node["category"])
    
    categories = []
    for i, cat_name in enumerate(categories_set):
        categories.append({
            "name": cat_name,
            "itemStyle": {
                "color": f"hsl({i * 360 / len(categories_set)}, 70%, 60%)"
            }
        })
    
    nodes = list(nodes_dict.values())
    
    return {
        "nodes": nodes,  # Limit for better visual effects
        "links": links,
        "categories": categories,
        "stats": {
            "total_nodes": len(nodes),
            "total_edges": len(links),
            "displayed_nodes": len(nodes[:500]),
            "displayed_edges": len(links[:1000])
        }
    }


def clean_graphrag_format(graph_data,remove_unclassed_entity=True,cats_allowed=[]):
    """Convert GraphRAG relationship list to ECharts format"""
    nodes_dict = {}
    links = []
    
    # Extract nodes and relationships from the list
    for item in graph_data:
        if not isinstance(item, dict):
            continue
            
        start_node = item.get("start_node", {})
        end_node = item.get("end_node", {})
        relation = item.get("relation", "related_to")
        
        # Process start node
        start_id = ""
        end_id = ""
        if start_node:
            start_id = start_node.get("properties", {}).get("name", "")
            cat = start_node.get("properties", {}).get("schema_type", start_node.get("label", "entity"))
            if (cat=='entity' and remove_unclassed_entity) or (cat not in cats_allowed):
                start_id = ""
            else:
                nodes_dict[start_id] = {
                    "id": start_id,
                    "name": start_id[:30],
                    "category": start_node.get("properties", {}).get("schema_type", start_node.get("label", "entity")),
                    "symbolSize": 25,
                    "properties": start_node.get("properties", {})
                }
        # Process end node
        if end_node:
            end_id = end_node.get("properties", {}).get("name", "")
            cat = end_node.get("properties", {}).get("schema_type", end_node.get("label", "entity"))
            if (cat=='entity' and remove_unclassed_entity) or (cat not in cats_allowed):
                end_id = ""
            else:
                nodes_dict[end_id] = {
                    "id": end_id,
                    "name": end_id[:30],
                    "category": end_node.get("properties", {}).get("schema_type", end_node.get("label", "entity")),
                    "symbolSize": 25,
                    "properties": end_node.get("properties", {})
                }
        
        # Add relationship
        if start_id and end_id:
            links.append({
                "source": start_id,
                "target": end_id,
                "name": relation,
                "value": 1
            })
    
    # Create categories
    categories_set = set()
    for node in nodes_dict.values():
        categories_set.add(node["category"])
    
    categories = []
    for i, cat_name in enumerate(categories_set):
        categories.append({
            "name": cat_name,
            "itemStyle": {
                "color": f"hsl({i * 360 / len(categories_set)}, 70%, 60%)"
            }
        })
    
    nodes = list(nodes_dict.values())
    
    return {
        "nodes": nodes,  # Limit for better visual effects​​
        "links": links,
        "categories": categories,
        "stats": {
            "total_nodes": len(nodes),
            "total_edges": len(links),
            "displayed_nodes": len(nodes[:500]),
            "displayed_edges": len(links[:1000])
        }
    }


def graph_stats(graph):
    ### Count nodes and edges
    print(f"Number of Nodes:{graph.number_of_nodes()}")
    print(f"Number of edges:{graph.number_of_edges()}")
    ### degree distribution
    degrees = pd.Series([x[1] for x in list(graph.degree)])
    print(f"Degree stats: mean={degrees.mean()}, median={degrees.median()}, lower_quantile={degrees.quantile(0.25)}, higher_quantile={degrees.quantile(0.75)}, std={degrees.std()}")
    print(f"Degree counts:")
    print(degrees.value_counts().sort_index()[:5])
    print(f"...")
    print(degrees.value_counts().sort_index()[-5:])
    try:
        print(f"Clustering coef (called transitivity in networkx):{nx.transitivity(graph)}")
    except Exception as e:
        if "multigraph" in str(e):
            print("Multigraph detected. Skipping clustering coef")
        else:
            print("Unknown error occured. Skipping clustering coef")
    if nx.is_connected(graph):
        print(f"Diameter: {nx.diameter(graph)}")
    else:
        print(f"Graph is not connected. Numer of components: {nx.number_connected_components(graph)}")


def deg_hist(graph,bins=50,limit=50):
    degrees = pd.Series([x[1] for x in list(graph.degree)])
    plt.hist(degrees,bins=bins,range=(0,limit))
    plt.show()

def print_neighbors(graph,node):
    neighbors = list(graph.neighbors(node))
    print(f"Number of neighbors: {len(neighbors)}")
    for neighbor in neighbors:
        print(f"Neighbor: {neighbor}, Contents: {graph.nodes[neighbor]}, Edge: {graph[node][neighbor]}")

def sample_pairs(graph, n_linked = 5, n_non_linked = 5, seed = None):
    """
    Sample linked (connected by an edge) and non-linked (no direct edge) pairs of nodes.

    Args:
        graph:        A NetworkX graph
        n_linked:     Number of linked pairs to sample
        n_non_linked: Number of non-linked pairs to sample
        seed:         Random seed for reproducibility

    Returns:
        Dict with 'linked' and 'non_linked' lists of (node, node) tuples
    """
    if seed is not None:
        random.seed(seed)

    # --- Linked pairs: just sample from the edge list ---
    edges = list(graph.edges())
    if n_linked > len(edges):
        raise ValueError(f"Requested {n_linked} linked pairs but graph only has {len(edges)} edges")

    linked_pairs = random.sample(edges, n_linked)

    # --- Non-linked pairs: sample until we find pairs with no edge ---
    nodes = list(graph.nodes())
    if len(nodes) < 2:
        raise ValueError("Graph must have at least 2 nodes")

    max_possible_non_links = (len(nodes) * (len(nodes) - 1)) // 2 - len(edges)
    if n_non_linked > max_possible_non_links:
        raise ValueError(
            f"Requested {n_non_linked} non-linked pairs but only {max_possible_non_links} exist"
        )

    non_linked_pairs = []
    seen = set()

    # Use rejection sampling — efficient when graph is sparse (most pairs are non-edges)
    while len(non_linked_pairs) < n_non_linked:
        u, v = random.sample(nodes, 2)
        pair = (min(u, v), max(u, v))  # canonical form to avoid (a,b) vs (b,a) duplicates
        if pair not in seen and not graph.has_edge(u, v):
            seen.add(pair)
            non_linked_pairs.append(pair)

    return {
        "linked":     linked_pairs,
        "non_linked": non_linked_pairs,
    }


from collections import defaultdict

class BookSearcher:
    """
    Finds closest distance (in characters) between any two substrings in a text.
    
    - Does NOT pre-scan the entire text up front
    - Lazily scans for each name on first query, then caches all its positions
    - Further queries reuse the cache with no re-scanning
    """

    def __init__(self, text: str):
        self.text = text
        self._cache: dict[str, list[int]] = {}  # name -> sorted list of start indices

    def _scan(self, name: str) -> list[int]:
        """Find all start positions of name in text, cache and return them."""
        if name in self._cache:
            return self._cache[name]

        positions = []
        start = 0
        while True:
            idx = self.text.find(name, start)
            if idx == -1:
                break
            positions.append(idx)
            start = idx + 1  # allows overlapping matches

        self._cache[name] = positions
        return positions

    def closest_distance(self, name1: str, name2: str) -> int:
        """
        Return the closest distance (in characters) between any occurrence
        of name1 and name2 in the text. Returns -1 if either is absent.
        Distance is measured start-index to start-index.
        """
        positions1 = self._scan(name1)
        positions2 = self._scan(name2)

        if not positions1 or not positions2:
            return -1

        # Two-pointer scan over sorted position lists
        min_distance = float('inf')
        i = j = 0

        while i < len(positions1) and j < len(positions2):
            distance = abs(positions1[i] - positions2[j])
            min_distance = min(min_distance, distance)
            if positions1[i] < positions2[j]:
                i += 1
            else:
                j += 1

        return min_distance

    def cache_info(self) -> dict:
        return {name: len(pos) for name, pos in self._cache.items()}


