"""
Flask Web Application for Social Network Analysis
MTech CSE Project - NIT
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from graph_builder import build_friendship_graph
from interest_matcher import build_interest_index
from recommender import FriendRecommender

app = Flask(__name__)

# Global variables to store loaded data
graph = None
recommender = None
is_initialized = False

def initialize_system():
    """Load data once when server starts"""
    global graph, recommender, is_initialized
    
    if is_initialized:
        return
    
    print("\n🚀 Initializing Social Network System...")
    print("   This may take a few minutes on first load...\n")
    
    try:
        # Build graph
        graph = build_friendship_graph()
        
        # Build interest index
        trie, profiles, interests = build_interest_index()
        
        # Create recommender
        recommender = FriendRecommender(graph, trie, interests)
        
        is_initialized = True
        print("\n✅ System ready! Starting web server...\n")
        
    except Exception as e:
        print(f"\n❌ Error initializing system: {e}")
        import traceback
        traceback.print_exc()
        raise

@app.route('/')
def home():
    """Main page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_user():
    """API endpoint to analyze a user"""
    
    if not is_initialized:
        return jsonify({'error': 'System not initialized'}), 500
    
    try:
        data = request.get_json()
        user_id = int(data.get('user_id', 0))
        
        if user_id <= 0:
            return jsonify({'error': 'Invalid user ID'}), 400
        
        # Check if user exists
        if not recommender.graph.has_node(user_id):
            return jsonify({
                'error': f'User {user_id} not found in the network',
                'exists': False
            }), 404
        
        # Get current friends
        friends = recommender.get_current_friends(user_id)
        
        # Get friend recommendations
        friend_recs = recommender.recommend_by_friends(user_id, top_k=10)
        
        # Get interest-based influencers
        influencers = recommender.get_top_influencers_by_interest(user_id, top_k=5)
        
        # Format response - Convert all numpy/pandas types to native Python types
        response = {
            'user_id': int(user_id),
            'exists': True,
            'current_friends': {
                'count': int(len(friends)),
                'list': [int(f) for f in friends[:20]]  # Convert each to native int
            },
            'recommended_friends': [
                {
                    'user_id': int(uid),
                    'mutual_count': int(count),
                    'reason': f'{int(count)} mutual friends'
                }
                for count, uid in friend_recs
            ],
            'top_influencers': [
                {
                    'user_id': int(uid),
                    'followers': int(degree),
                    'reason': f'{int(degree)} connections (highly influential)'
                }
                for degree, uid in influencers
            ],
            'stats': {
                'total_users': int(recommender.graph.num_nodes()),
                'total_edges': int(recommender.graph.num_edges_count())
            }
        }
        
        return jsonify(response)
        
    except ValueError:
        return jsonify({'error': 'User ID must be a number'}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()  # Print error details to console
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get overall network statistics"""
    
    if not is_initialized:
        return jsonify({'error': 'System not initialized'}), 500
    
    try:
        total_nodes = int(recommender.graph.num_nodes())
        total_edges = int(recommender.graph.num_edges_count())
        avg_degree = round(total_edges / total_nodes, 2) if total_nodes > 0 else 0
        
        return jsonify({
            'total_users': total_nodes,
            'total_friendships': total_edges,
            'avg_friends_per_user': float(avg_degree)
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize system before starting server
    try:
        initialize_system()
        
        # Start Flask server
        print("=" * 70)
        print("🌐 WEB SERVER RUNNING")
        print("=" * 70)
        print("\n   Open your browser and go to:")
        print("   👉 http://127.0.0.1:5000\n")
        print("   Press Ctrl+C to stop the server\n")
        print("=" * 70 + "\n")
        
        app.run(debug=False, host='127.0.0.1', port=5000)
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")
        import traceback
        traceback.print_exc()
