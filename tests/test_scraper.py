import unittest
from src.scraper import NewsScraper
from src.utils import load_config

class TestNewsScraper(unittest.TestCase):
    def setUp(self):
        config = load_config('config/config.yaml')
        self.scraper = NewsScraper(config)

    def test_contains_money(self):
        self.assertTrue(self.scraper.contains_money("The amount is $100.00"))
        self.assertFalse(self.scraper.contains_money("There is no money mentioned"))

if __name__ == '__main__':
    unittest.main()
