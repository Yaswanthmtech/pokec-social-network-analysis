"""Configuration settings"""

# File paths
EDGES_FILE = 'data/datasets/soc-pokec-relationships.txt'
PROFILES_FILE = 'data/datasets/soc-pokec-profiles.txt'

# Sampling (for testing - set to None for full dataset)
MAX_EDGES = 5000     # Start with 500K edges for speed
MAX_PROFILES = 2000   # 200K profiles

# Recommendation settings
TOP_K_RECOMMENDATIONS = 10
TOP_K_INFLUENCERS = 5
