import unittest
from app import app

class MovieWebTestCase(unittest.TestCase):
    """
    Unit test class for testing the Flask movie web application.

    This class contains test cases to verify the behavior of various routes in the application,
    including testing the homepage and adding a new movie.
    """

    def setUp(self):
        """
        Sets up the test client for the Flask application.

        This method is called before each test case to configure the app for testing mode
        and create a test client to simulate HTTP requests.
        """
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_homepage(self):
        """
        Tests the homepage route ('/').

        This test case sends a GET request to the homepage and verifies that the response status
        code is 200 (OK) and that the text 'All Users' is present in the HTML content.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Users', response.data)

    def test_add_movie(self):
        """
        Tests adding a new movie for a user via the '/add_movie/<int:user_id>' route.

        This test case sends a POST request with movie data (name, director, year, rating)
        to add a new movie to a specific user (user ID 1) and follows the redirect to the user's
        movie list page. It verifies that the response status code is 200 and that the newly added
        movie name ('Inception') is present in the HTML content.
        """
        response = self.client.post('/add_movie/1', data=dict(
            name="Inception",
            director="Christopher Nolan",
            year=2010,
            rating=9.0
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Inception', response.data)

if __name__ == '__main__':
    """
    Runs the test cases when the script is executed directly.

    This is the entry point for running the unit tests, and it will execute all defined test cases.
    """
    unittest.main()
