import unittest
import sys
import os

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from indexer import Indexer

class TestIndexer(unittest.TestCase):
    def test_build_index(self):
        indexer = Indexer()
        mock_data = {
            "http://example.com/1": "Good friends are good",
            "http://example.com/2": "Indifference is bad"
        }
        
        indexer.build_index(mock_data)
        
        # Test case insensitivity and positions
        self.assertIn("good", indexer.index)
        self.assertEqual(indexer.index["good"]["http://example.com/1"], [0, 3])
        self.assertIn("indifference", indexer.index)

if __name__ == "__main__":
    unittest.main()