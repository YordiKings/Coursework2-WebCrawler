import unittest
import sys
import os

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from indexer import Indexer

class TestIndexer(unittest.TestCase):
    def test_build_index_standard_words(self):
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

    def test_build_index_with_apostrophes(self):
        indexer = Indexer()
        mock_data = {
            "http://example.com/3": "That's why it's important."
        }
        
        indexer.build_index(mock_data)
        
        # Test that words with apostrophes are captured as single tokens
        self.assertIn("that's", indexer.index)
        self.assertIn("it's", indexer.index)
        
        # Ensure it didn't break them into 'that', 's', 'it', 's'
        self.assertNotIn("s", indexer.index)
        
        # Verify correct positions
        self.assertEqual(indexer.index["that's"]["http://example.com/3"], [0])
        self.assertEqual(indexer.index["it's"]["http://example.com/3"], [2])

if __name__ == "__main__":
    unittest.main()