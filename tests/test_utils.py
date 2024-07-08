import unittest
from src.utils import load_config, save_to_excel
import os
import pandas as pd

class TestUtils(unittest.TestCase):
    def test_load_config(self):
        config = load_config('config/config.yaml')
        self.assertIn('robocloud', config)

    def test_save_to_excel(self):
        data = [{'title': 'Sample News', 'date': '2023-07-01', 'description': 'This is a test.', 'picture_filename': '', 'search_count': 1, 'contains_money': False}]
        save_to_excel(data, 'output/test.xlsx')
        self.assertTrue(os.path.exists('output/test.xlsx'))
        df = pd.read_excel('output/test.xlsx')
        self.assertEqual(df.iloc[0]['title'], 'Sample News')

if __name__ == '__main__':
    unittest.main()
