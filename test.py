import os
from os import path
from app import app
import unittest


if path.exists('env.py'):
    import env


class loginTest(unittest.TestCase):

    # Ensure the /users/login page loads correctly
    def test_login(self):
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
            username="test-account", password="Test123"), follow_redirects=True)
        response = tester.get('/users/logout', follow_redirects=True)
        self.assertTrue(b'You were successfully logged Out' in response.data)


if __name__ == '__main__':
    app.secret_key = os.getenv('SECRET_KEY')
    unittest.main()
