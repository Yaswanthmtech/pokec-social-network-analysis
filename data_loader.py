"""Load data from Pokec dataset files"""

import pandas as pd
import os
from config import EDGES_FILE, PROFILES_FILE, MAX_EDGES, MAX_PROFILES

def load_edges(max_rows=MAX_EDGES):
    """
    Load friendship edges from file.
    Returns: DataFrame with columns ['u', 'v']
    """
    
    if not os.path.exists(EDGES_FILE):
        raise FileNotFoundError(f"Edges file not found: {EDGES_FILE}")
    
    print(f"\n📂 Loading edges from {EDGES_FILE}...")
    print(f"   Reading up to {max_rows:,} edges..." if max_rows else "   Reading all edges...")
    
    try:
        df = pd.read_csv(
            EDGES_FILE,
            sep='\t',
            header=None,
            names=['u', 'v'],
            nrows=max_rows,
            dtype={'u': 'int32', 'v': 'int32'},
            on_bad_lines='skip'
        )
    except TypeError:
        # Older pandas version
        df = pd.read_csv(
            EDGES_FILE,
            sep='\t',
            header=None,
            names=['u', 'v'],
            nrows=max_rows,
            dtype={'u': 'int32', 'v': 'int32'},
            error_bad_lines=False
        )
    
    print(f"✓ Loaded {len(df):,} edges")
    print(f"   Unique users: {len(set(df['u']) | set(df['v'])):,}")
    
    return df


def load_profiles(max_rows=MAX_PROFILES):
    """
    Load user profiles from file.
    Returns: DataFrame with user_id, region, and interests
    """
    
    if not os.path.exists(PROFILES_FILE):
        raise FileNotFoundError(f"Profiles file not found: {PROFILES_FILE}")
    
    print(f"\n📂 Loading profiles from {PROFILES_FILE}...")
    print(f"   Reading up to {max_rows:,} profiles..." if max_rows else "   Reading all profiles...")
    
    # Only load essential columns for speed
    usecols = [0, 4, 11]  # user_id, region, hobbies
    
    try:
        df = pd.read_csv(
            PROFILES_FILE,
            sep='\t',
            header=None,
            names=['user_id', 'region', 'interests'],
            usecols=usecols,
            nrows=max_rows,
            dtype='string',
            on_bad_lines='skip'
        )
    except TypeError:
        df = pd.read_csv(
            PROFILES_FILE,
            sep='\t',
            header=None,
            names=['user_id', 'region', 'interests'],
            usecols=usecols,
            nrows=max_rows,
            dtype='string',
            error_bad_lines=False
        )
    
    # Convert user_id to int
    df['user_id'] = pd.to_numeric(df['user_id'], errors='coerce')
    df = df.dropna(subset=['user_id'])
    df['user_id'] = df['user_id'].astype('int32')
    
    # Replace 'null' with empty string
    df['region'] = df['region'].fillna('').replace('null', '')
    df['interests'] = df['interests'].fillna('').replace('null', '')
    
    print(f"✓ Loaded {len(df):,} profiles")
    
    return df


print("✓ Data loader module ready")
