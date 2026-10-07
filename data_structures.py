"""Core data structures used in the project"""

import heapq
from collections import defaultdict

class MaxHeap:
    """Max heap for top-K recommendations"""
    
    def __init__(self):
        self.heap = []
    
    def push(self, score, user_id):
        """Add item with score"""
        heapq.heappush(self.heap, (-score, user_id))
    
    def pop(self):
        """Remove and return highest score item"""
        if self.heap:
            neg_score, user_id = heapq.heappop(self.heap)
            return -neg_score, user_id
        return None
    
    def get_top_k(self, k):
        """Extract top K items"""
        results = []
        temp = []
        
        for _ in range(min(k, len(self.heap))):
            if not self.heap:
                break
            item = heapq.heappop(self.heap)
            results.append((-item[0], item[1]))
            temp.append(item)
        
        # Restore heap
        for item in temp:
            heapq.heappush(self.heap, item)
        
        return results
    
    def __len__(self):
        return len(self.heap)


class TrieNode:
    """Node in Trie for interest matching"""
    
    def __init__(self):
        self.children = {}
        self.users = set()
        self.is_end = False


class Trie:
    """Trie for fast interest-based user search"""
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word, user_id):
        """Insert word and associate with user_id"""
        if not word:
            return
        
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end = True
        node.users.add(user_id)
    
    def find_users_with_prefix(self, prefix):
        """Find all users with interests starting with prefix"""
        if not prefix:
            return set()
        
        node = self.root
        
        for char in prefix.lower():
            if char not in node.children:
                return set()
            node = node.children[char]
        
        users = set()
        self._collect_users(node, users)
        return users
    
    def _collect_users(self, node, users):
        """Recursively collect user IDs"""
        if node.is_end:
            users.update(node.users)
        
        for child in node.children.values():
            self._collect_users(child, users)


class AdjacencyListGraph:
    """Graph using adjacency list (dictionary)"""
    
    def __init__(self):
        self.graph = defaultdict(set)
        self.num_edges = 0
    
    def add_edge(self, u, v):
        """Add directed edge from u to v"""
        if v not in self.graph[u]:
            self.graph[u].add(v)
            self.num_edges += 1
    
    def get_neighbors(self, u):
        """Get friends of user u - O(1)"""
        return self.graph.get(u, set())
    
    def has_node(self, u):
        """Check if user exists"""
        return u in self.graph
    
    def num_nodes(self):
        """Count total users"""
        return len(self.graph)
    
    def num_edges_count(self):
        """Count total edges"""
        return self.num_edges


print("✓ Data structures module loaded")
