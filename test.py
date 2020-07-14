import os
from os import path
from app import app
import unittest


if path.exists('env.py'):
    import env


# Check if the Login Feature is working
class loginTest(unittest.TestCase):

    # Ensure the /users/login page loads correctly
    def test_login_page(self):
        tester = app.test_client(self)
        response = tester.get('/users/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure the /users/login content loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/users/login', content_type='html/text')
        self.assertTrue(b'Dont have an account?' in response.data)

    # Ensure the Login function is working correctly and redirects correctly
    def test_login_success(self):
        tester = app.test_client(self)
        response = tester.post('/users/login/check', data=dict(
            username="test-account", password="Test123"), follow_redirects=True)
        self.assertTrue(b'You were successfully logged in' in response.data)

    # Ensure the Logout function is working correctly
    #  and redirects correctly
    def test_logout_success(self):
        tester = app.test_client(self)
        tester.post('/users/login/check', data=dict(
            username="test-account", password="Test123"))
        response = tester.get('/users/logout', follow_redirects=True)
        self.assertTrue(b'You were successfully logged Out' in response.data)


# Check if all routes that require login are acting as intended
class loginRequired(unittest.TestCase):

    # check add game requires login
    def test_login_required_games(self):
        tester = app.test_client(self)
        response = tester.get('/games/add', follow_redirects=True,
                              content_type='html/text')
        self.assertTrue(b'Please login to access this feature'
                        in response.data)

    # Check add review requires login
    def test_login_required_review(self):
        tester = app.test_client(self)
        response = tester.get('/review/add', follow_redirects=True,
                              content_type='html/text')
        self.assertTrue(b'Please login to access this feature'
                        in response.data)

    # Check add developer requires login
    def test_login_required_developer(self):
        tester = app.test_client(self)
        response = tester.get('/developer/add', follow_redirects=True,
                              content_type='html/text')
        self.assertTrue(b'Please login to access this feature'
                        in response.data)

    # Check add publisher requires login
    def test_login_required_publisher(self):
        tester = app.test_client(self)
        response = tester.get('/developer/add', follow_redirects=True,
                              content_type='html/text')
        self.assertTrue(b'Please login to access this feature'
                        in response.data)

    # Check add publisher requires login
    def test_login_required_category(self):
        tester = app.test_client(self)
        response = tester.get('/category/add', follow_redirects=True,
                              content_type='html/text')
        self.assertTrue(b'Please login to access this feature'
                        in response.data)

    # Check add admin_panel requires login as admin
    def test_login_required_admin(self):
        tester = app.test_client(self)
        response = tester.get('/adminpanel', follow_redirects=True,
                              content_type='html/text')
        self.assertTrue(b'Please Log In as Administrator to access this page'
                        in response.data)


# Logs in then checks if the redirect works and
# provides the correct HTTP code
class add_http_codes(unittest.TestCase):

    def test_game_add_http(self):
        tester = app.test_client(self)
        tester.post('/users/login/check', data=dict(
            username="test-account", password="Test123"))
        response = tester.get(
            '/games/add', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_review_add_http(self):
        tester = app.test_client(self)
        tester.post('/users/login/check', data=dict(
            username="test-account", password="Test123"))
        response = tester.get(
            '/review/add', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_developer_add_http(self):
        tester = app.test_client(self)
        tester.post('/users/login/check', data=dict(
            username="test-account", password="Test123"))
        response = tester.get(
            '/developer/add', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_publisher_add_http(self):
        tester = app.test_client(self)
        tester.post('/users/login/check', data=dict(
            username="test-account", password="Test123"))
        response = tester.get(
            '/publisher/add', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    app.secret_key = os.getenv('SECRET_KEY')
    unittest.main()
