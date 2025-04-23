import unittest
import numpy as np
import cv2
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.image_utils import enhance_image, segment_image

class TestImageUtils(unittest.TestCase):
    def setUp(self):
        # Create a sample test image
        self.test_image = np.zeros((100, 100), dtype=np.uint8)
        # Add some features to test image
        self.test_image[25:75, 25:75] = 200
        
    def test_enhance_image(self):
        # Test image enhancement
        enhanced = enhance_image(self.test_image)
        self.assertIsNotNone(enhanced)
        self.assertEqual(enhanced.shape, self.test_image.shape)
        
    def test_segment_image(self):
        # Test image segmentation
        segmented = segment_image(self.test_image)
        self.assertIsNotNone(segmented)
        self.assertEqual(segmented.shape, self.test_image.shape)
        # Verify binary output
        unique_values = np.unique(segmented)
        self.assertTrue(all(val in [0, 255] for val in unique_values))

if __name__ == '__main__':
    unittest.main()