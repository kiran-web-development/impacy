import unittest
import sys
import os
import io
import json
from PIL import Image
import numpy as np

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.app import app

class TestFlaskAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Create a test image
        img = Image.fromarray(np.zeros((100, 100), dtype=np.uint8))
        self.test_image_io = io.BytesIO()
        img.save(self.test_image_io, 'PNG')
        self.test_image_io.seek(0)
        
    def test_health_check(self):
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        
    def test_analyze_no_image(self):
        response = self.app.post('/api/analyze')
        self.assertEqual(response.status_code, 400)
        
    def test_analyze_with_image(self):
        data = {'image': (self.test_image_io, 'test.png')}
        response = self.app.post('/api/analyze',
                               content_type='multipart/form-data',
                               data=data)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['status'], 'success')
        self.assertIn('details', result)

if __name__ == '__main__':
    unittest.main()