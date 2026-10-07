"""Friend recommendation system"""

from collections import Counter
from data_structures import MaxHeap

class FriendRecommender:
    """Complete recommendation system"""
    
    def __init__(self, graph, interest_trie, user_interests):
        self.graph = graph
        self.trie = interest_trie
        self.user_interests = user_interests
    
    def get_current_friends(self, user_id):
        """Get list of current friends"""
        return list(self.graph.get_neighbors(user_id))
    
    def recommend_by_friends(self, user_id, top_k=10):
        """
        Friend-of-friend recommendations.
        Returns: List of (user_id, mutual_count) tuples
        """
        
        my_friends = self.graph.get_neighbors(user_id)
        
        if not my_friends:
            return []
        
        # Count mutual friends
        mutual_count = Counter()
        
        for friend in my_friends:
            friend_of_friend = self.graph.get_neighbors(friend)
            
            for candidate in friend_of_friend:
                if candidate != user_id and candidate not in my_friends:
                    mutual_count[candidate] += 1
        
        # Use heap to get top K
        heap = MaxHeap()
        for candidate, count in mutual_count.items():
            heap.push(count, candidate)
        
        return heap.get_top_k(top_k)
    
    def recommend_by_interests(self, user_id, top_k=5):
        """
        Interest-based recommendations using Trie.
        Returns: List of (user_id, match_score) tuples
        """
        
        my_interests = self.user_interests.get(user_id, set())
        
        if not my_interests:
            return []
        
        # Find users with matching interests
        similar_users = Counter()
        
        for interest in my_interests:
            # Use first 3 chars as prefix
            prefix = interest[:min(3, len(interest))]
            matching_users = self.trie.find_users_with_prefix(prefix)
            
            for candidate in matching_users:
                if candidate != user_id:
                    similar_users[candidate] += 1
        
        # Get top K
        heap = MaxHeap()
        for candidate, score in similar_users.items():
            heap.push(score, candidate)
        
        return heap.get_top_k(top_k)
    
    def get_top_influencers_by_interest(self, user_id, top_k=5):
        """
        Find top influencers with similar interests.
        Returns: List of (user_id, score) tuples
        """
        
        # Get users with similar interests
        similar = self.recommend_by_interests(user_id, top_k=50)
        
        if not similar:
            return []
        
        similar_user_ids = {uid for _, uid in similar}
        
        # Rank by degree (popularity) among similar users
        heap = MaxHeap()
        
        for uid in similar_user_ids:
            degree = len(self.graph.get_neighbors(uid))
            heap.push(degree, uid)
        
        return heap.get_top_k(top_k)


print("✓ Recommender module ready")
