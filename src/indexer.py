import json
import re
import os
from collections import defaultdict

INDEX_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "index.json")

class Indexer:
    def __init__(self):
        # Data structure: dict[word] -> dict[url] -> list[positions]
        self.index = defaultdict(lambda: defaultdict(list))

    def build_index(self, pages_data):
        self.index.clear()
        for url, text in pages_data.items():
            # Extract words using regex (alphanumeric sequences)
            words = re.findall(r'\b\w+\b', text.lower())
            
            for position, word in enumerate(words):
                self.index[word][url].append(position)

    def save(self):
        # Ensure data directory exists
        os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
        
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            # Convert defaultdict to a standard dict for JSON serialization
            serializable_index = {word: dict(urls) for word, urls in self.index.items()}
            json.dump(serializable_index, f, indent=4)
        print(f"Index successfully saved to {INDEX_FILE}")

    def load(self):
        if not os.path.exists(INDEX_FILE):
            print(f"Error: Index file not found at {INDEX_FILE}. Run 'build' first.")
            return False
            
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Reconstruct the defaultdict
            self.index = defaultdict(lambda: defaultdict(list), data)
        print("Index loaded successfully.")
        return True