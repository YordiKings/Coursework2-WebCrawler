import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from crawler import crawl

class TestCrawler(unittest.TestCase):
    
    @patch('crawler.time.sleep')  # Mocks the 6-second politeness delay
    @patch('crawler.requests.get') # Mocks the HTTP request
    def test_crawl_single_page(self, mock_get, mock_sleep):
        # Set up a fake response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        # Provide a simple HTML string without a 'next' button so the crawler stops after one page
        mock_response.text = '<html><body><span class="text">A good mock quote.</span></body></html>'
        mock_get.return_value = mock_response

        # Execute the crawler
        pages_data = crawl()

        # Assertions to ensure it crawled our mocked root URL and extracted text
        expected_url = "https://quotes.toscrape.com/"
        self.assertIn(expected_url, pages_data)
        self.assertIn("A good mock quote.", pages_data[expected_url])
        
        # Verify that our politeness window was actually triggered in the code
        mock_sleep.assert_called_with(6)

if __name__ == "__main__":
    unittest.main()