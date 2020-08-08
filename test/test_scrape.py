import unittest
import sys
sys.path.append('C:/Users/15314/source/repos/WebScraping/')
from Scrapers import scrapfunctions as sp



class TestGetPageResponse(unittest.TestCase):
    """lolol"""

    def test_response_none(self):
        """Test that a bogus url returns none"""
        bogus_url = 'https://stupid5757bogushahaha57.com/lolol'
        response = sp.get_page_response(bogus_url)

        self.assertIsNone(response, 'An obviously stupid url returned a page response.. Check it out please.')


    def test_urls(self):
        """Test that a few of the basic urls are still returning page responses."""
        urls = ["https://www.oaktreecapital.com/insights/howard-marks-memos",
                "https://guides.loc.gov/federalist-papers/full-text",
        ]

        responses = []
        for url in urls:
            responses.append(sp.get_page_response(url))
        
        self.assertEqual(all(responses), True , 'One of the urls did not return a response object. That sucks!')



if __name__ == '__main__':
    unittest.main()