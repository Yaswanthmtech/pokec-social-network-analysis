"""Build interest-based matching using Trie"""

from data_structures import Trie
from data_loader import load_profiles
import re

WORD_PATTERN = re.compile(r'[a-zA-Z]{3,}')

def build_interest_index():
    """
    Build Trie index for interest-based matching.
    Returns: (Trie, user_profiles dict, user_interests dict)
    """
    
    print("\n🔍 Building interest index...")
    
    profiles_df = load_profiles()
    
    trie = Trie()
    user_profiles = {}
    user_interests = {}
    
    print("   Processing user interests...")
    
    for idx, row in profiles_df.iterrows():
        user_id = row['user_id']
        interests_text = str(row['interests'])
        region = str(row['region'])
        
        # Extract interest keywords
        words = WORD_PATTERN.findall(interests_text.lower())
        interest_set = set(words)
        
        # Store for later
        user_profiles[user_id] = {
            'region': region,
            'interests': interest_set
        }
        user_interests[user_id] = interest_set
        
        # Add to Trie
        for word in interest_set:
            trie.insert(word, user_id)
        
        if (idx + 1) % 50000 == 0:
            print(f"   Processed {idx+1:,} profiles...")
    
    print(f"\n✓ Interest index built!")
    print(f"   Users with interests: {len(user_interests):,}")
    
    return trie, user_profiles, user_interests


print("✓ Interest matcher module ready")
