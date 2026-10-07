# Social Network Analysis & Friend Recommendation System

A scalable social network analysis and friend recommendation system developed as an M.Tech Computer Science & Engineering project.

The system analyzes friendship relationships and user interests to generate relevant friend recommendations using classical data structures and algorithms.

---
## Dataset

The project uses the Pokec social network dataset containing friendship relationships and user profile information.

The complete raw dataset is **not included in this repository because of its large size**.

The required dataset files must be placed in the appropriate local data directory before running the project.

## Overview

Social networks contain millions of users and relationships, making efficient graph representation and recommendation algorithms essential.

This project uses the Pokec social network dataset to demonstrate how graphs, hash maps, tries, and heaps can be combined to perform efficient social-network analysis and friend recommendation.

The system provides both:

- Command Line Interface (CLI)
- Flask-based Web Interface

---

## Features

- Social network graph construction
- Efficient user lookup
- Friend-of-friend recommendation
- Interest-based friend recommendation
- Trie-based interest matching
- Max Heap-based recommendation ranking
- Top influencer identification
- CLI-based analysis
- Web-based interactive interface
- Handling of invalid or missing user IDs

---

## Technology Stack
Python 3
Flask
Pandas
NetworkX
Hash Maps
Graph / Adjacency Lists
Trie
Max Heap

--

## Data Structures

### Hash Map

Used for efficient user profile and relationship lookup.

### Adjacency List

Used to represent the friendship graph efficiently.

### Trie

Used for interest-based matching and prefix searching.

### Max Heap

Used for ranking and retrieving high-scoring recommendations.

---

## Algorithms

### Friend-of-Friend Recommendation

The system examines the friends of a selected user and then explores their connections.

Mutual friends are counted and used as a recommendation score.

### Interest Matching

The interests of users are indexed using a Trie.

Users sharing common interests can then be identified efficiently.

### Recommendation Ranking

Recommendation candidates are ranked according to their scores using a Max Heap.

### Top Influencers

Users with similar interests can be ranked according to their number of connections.

---

## System Architecture

```text
                    User
                     |
              +------+------+
              |             |
             CLI        Web Interface
              |             |
              +------+------+
                     |
                Data Loader
                     |
          +----------+----------+
          |                     |
     User Profiles        Friendship Data
          |                     |
          |                Graph Builder
          |                     |
          |                Adjacency List
          |                     |
          +----------+----------+
                     |
             Recommendation Engine
                     |
          +----------+----------+
          |                     |
   Friend-of-Friend       Interest Matching
          |                     |
          |                    Trie
          |                     |
          +----------+----------+
                     |
              Recommendation
                  Ranking
                     |
                  Max Heap
                     |
             Recommended Friends

----
## How to Run
1. Clone the Repository
git clone https://github.com/Yaswanthmech/pokec-social-network-analysis.git
cd pokec-social-network-analysis

2. Install Dependencies
pip install -r requirements.txt

3. Run the CLI
python main.py

4. Run the Web Application
python app.py

Then open:
http://localhost:5000

CLI Usage
The CLI allows a user to enter a User ID and analyze the corresponding social-network information.
The system can display:
- Current friends
- Recommended friends
- Mutual-friend scores
- Users with similar interests
- Top influencers
Web Application
The Flask web application provides an interactive interface for analyzing users.
The interface allows the user to enter a User ID and view:
- User information
- Current friends
- Friend recommendations
- Top influencers with similar interests

---
## Author
Yaswanth Pathinavalasa
