import unittest
from unittest.mock import patch
import sys
import os
import io

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from search import SearchEngine

# We create a fake Indexer class to inject into our SearchEngine
class MockIndexer:
    def __init__(self):
        # A hardcoded dummy index
        self.index = {
            "good": {"http://test.com/1": [0, 5]},
            "friends": {"http://test.com/1": [1], "http://test.com/2": [0]}
        }

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.mock_indexer = MockIndexer()
        self.search_engine = SearchEngine(self.mock_indexer)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_find_phrase_success(self, mock_stdout):
        # Searching for 'good friends' should only return http://test.com/1
        # because http://test.com/2 only contains 'friends', not 'good'.
        self.search_engine.find_phrase("good friends")
        
        output = mock_stdout.getvalue()
        self.assertIn("http://test.com/1", output)
        self.assertNotIn("http://test.com/2", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_find_phrase_not_found(self, mock_stdout):
        # Searching for a word not in the mock index
        self.search_engine.find_phrase("nonsense")
        
        output = mock_stdout.getvalue()
        self.assertIn("No pages found containing the word 'nonsense'", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_word(self, mock_stdout):
        # Testing the 'print <word>' functionality
        self.search_engine.print_word("good")
        
        output = mock_stdout.getvalue()
        self.assertIn("http://test.com/1", output)
        self.assertIn("Frequency: 2", output) 

if __name__ == "__main__":
    unittest.main()