"""
Main application - Social Network Analysis & Recommendation System
MTech CSE Project - NIT
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from graph_builder import build_friendship_graph
from interest_matcher import build_interest_index
from recommender import FriendRecommender

def display_banner():
    """Show project banner"""
    print("\n" + "=" * 70)
    print("  SOCIAL NETWORK ANALYSIS & FRIEND RECOMMENDATION SYSTEM")
    print("  MTech CSE - Data Structures Project")
    print("  Dataset: Pokec Social Network (1.6M users, 30M edges)")
    print("=" * 70)

def display_user_info(user_id, recommender):
    """Display complete information for a user"""
    
    print("\n" + "=" * 70)
    print(f"  USER ANALYSIS: {user_id}")
    print("=" * 70)
    
    # Check if user exists
    if not recommender.graph.has_node(user_id):
        print(f"\n❌ Error: User {user_id} not found in the network.")
        return
    
    # 1. Current Friends
    print(f"\n👥 CURRENT FRIENDS:")
    friends = recommender.get_current_friends(user_id)
    
    if friends:
        print(f"   Total friends: {len(friends)}")
        print(f"   Friends list: {friends[:10]}")  # Show first 10
        if len(friends) > 10:
            print(f"   ... and {len(friends)-10} more")
    else:
        print("   No friends found (isolated user)")
    
    # 2. Recommended Friends
    print(f"\n✨ RECOMMENDED FRIENDS (Friend-of-Friend):")
    friend_recs = recommender.recommend_by_friends(user_id, top_k=10)
    
    if friend_recs:
        for i, (candidate, mutual_count) in enumerate(friend_recs, 1):
            print(f"   {i}. User {candidate:>8} - {mutual_count} mutual friends")
    else:
        print("   No recommendations available")
    
    # 3. Top Influencers with Similar Interests
    print(f"\n🌟 TOP INFLUENCERS WITH SIMILAR INTERESTS:")
    influencers = recommender.get_top_influencers_by_interest(user_id, top_k=5)
    
    if influencers:
        for i, (inf_id, degree) in enumerate(influencers, 1):
            print(f"   {i}. User {inf_id:>8} - {degree:>4} friends (highly connected)")
    else:
        print("   No influencers found (add interests to profile)")
    
    print("\n" + "=" * 70)

def main():
    """Main execution"""
    
    display_banner()
    
    try:
        # Step 1: Build graph
        graph = build_friendship_graph()
        
        # Step 2: Build interest index
        trie, profiles, interests = build_interest_index()
        
        # Step 3: Create recommender
        print("\n🚀 Initializing recommendation system...")
        recommender = FriendRecommender(graph, trie, interests)
        print("✓ System ready!")
        
        # Interactive mode
        print("\n" + "=" * 70)
        print("  INTERACTIVE MODE")
        print("  Enter user ID to analyze (or 'quit' to exit)")
        print("=" * 70)
        
        while True:
            try:
                user_input = input("\n👤 Enter User ID: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                user_id = int(user_input)
                display_user_info(user_id, recommender)
                
            except ValueError:
                print("❌ Invalid input. Please enter a numeric user ID.")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
    
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure dataset files are in data/datasets/")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
