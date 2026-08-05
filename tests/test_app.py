import os
import unittest
import io
from app import app

class FlaskAppSecurityTestCase(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        self.app = app.test_client()
        self.app.testing = True
        
        # Paths to programmatically generated test assets
        self.test_dir = os.path.join(os.path.dirname(__file__), 'test_images')
        self.real_img_path = os.path.join(self.test_dir, 'test_real.jpg')
        self.fake_img_path = os.path.join(self.test_dir, 'test_fake.png')
        self.malicious_img_path = os.path.join(self.test_dir, 'test_malicious.png')

    def test_index_page(self):
        """Verify the index page loads successfully and contains the original template's text."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload', response.data)

    def test_security_headers_present(self):
        """Verify that basic security headers are set on response to prevent XSS/Clickjacking."""
        response = self.app.get('/')
        self.assertEqual(response.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(response.headers.get('X-Frame-Options'), 'SAMEORIGIN')
        self.assertEqual(response.headers.get('X-XSS-Protection'), '1; mode=block')
        self.assertIn('Content-Security-Policy', response.headers)

    def test_upload_real_image_success(self):
        """Verify successful upload of a valid JPEG (representing real photograph)."""
        with open(self.real_img_path, 'rb') as img:
            data = {
                'image': (img, 'test_real.jpg')
            }
            response = self.app.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Result', response.data)

    def test_upload_fake_image_success(self):
        """Verify successful upload of a valid PNG (representing AI-generated image)."""
        with open(self.fake_img_path, 'rb') as img:
            data = {
                'image': (img, 'test_fake.png')
            }
            response = self.app.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Result', response.data)

    def test_upload_disguised_file_fails_signature(self):
        """Verify that a text file disguised as PNG fails magic byte signature checks and flashes warning."""
        with open(self.malicious_img_path, 'rb') as img:
            data = {
                'image': (img, 'test_malicious.png')
            }
            with self.app as client:
                response = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=False)
                self.assertEqual(response.status_code, 302)  # Check redirect back to home page
                
                # Check flash messages in the session
                with client.session_transaction() as session:
                    flashes = session.get('_flashes', [])
                    self.assertTrue(any('Security check failed' in msg for category, msg in flashes))

    def test_upload_unsupported_file_extension(self):
        """Verify that unsupported extensions (e.g. .txt) are rejected before signature checks and flash warning."""
        data = {
            'image': (io.BytesIO(b'dummy text'), 'test.txt')
        }
        with self.app as client:
            response = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=False)
            self.assertEqual(response.status_code, 302)
            
            with client.session_transaction() as session:
                flashes = session.get('_flashes', [])
                self.assertTrue(any('File type not allowed' in msg for category, msg in flashes))

    def test_upload_no_file(self):
        """Verify application behavior and session flash when no file is chosen."""
        data = {
            'image': (io.BytesIO(b''), '')
        }
        with self.app as client:
            response = client.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=False)
            self.assertEqual(response.status_code, 302)
            
            with client.session_transaction() as session:
                flashes = session.get('_flashes', [])
                self.assertTrue(any('No file selected' in msg for category, msg in flashes))

if __name__ == '__main__':
    unittest.main()
