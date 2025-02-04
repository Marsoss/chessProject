import sys
import os

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add parent directory to sys.path
sys.path.append(parent_dir)
import unittest
from chess_typing import Color, Square, Move, WHITE, BLACK

class TestColourFunctions(unittest.TestCase):
    def test_is_colour_valid(self):
        self.assertEqual(WHITE, 'white')
        self.assertEqual(BLACK, 'black')
        self.assertIsInstance(WHITE, Color)
        self.assertIsInstance(BLACK, Color)
        

    def test_is_colour_invalid(self):
        self.assertNotIsInstance('red', Color)
        self.assertNotIsInstance(123, Color)
        self.assertNotIsInstance(None, Color)

if __name__ == '__main__':
    unittest.main()
