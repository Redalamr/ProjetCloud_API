
import unittest 
from app import app

class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_healthz(self):
        response = self.app.get('/healthz')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'healthy', response.data)

    def test_readyz(self):
        response = self.app.get('/readyz')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ready', response.data)

    def test_api_events(self):
        response = self.app.get('/api/events')
        self.assertIn(response.status_code, [200, 500])

if __name__ == '__main__':
    unittest.main()