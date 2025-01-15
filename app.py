from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from data_manager import DataManager
from ai_features import AIFeatures
from dotenv import load_dotenv
import os
import logging

# Load environment variables from the .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)
data_manager = DataManager()
ai_features = AIFeatures()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Secret key for session and flash messages
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

@app.route('/')
def index():
    """
    Renders the homepage with a list of all users.

    This function retrieves all users from the DataManager and passes them to the 'index.html' template for display.

    Returns:
        A rendered HTML page displaying the list of users.
    """
    try:
        users = data_manager.get_all_users()
        return render_template('index.html', users=users)
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        flash('An error occurred while loading users.', 'error')
        return render_template('index.html', users=[])

@app.route('/user/<int:user_id>')
def user_movies(user_id):
    """
    Displays the movies associated with a specific user.

    This function retrieves the user by their ID, fetches all movies for that user, 
    and renders the 'movie_details.html' template with the user's details and movie list.

    Parameters:
        user_id (int): The ID of the user whose movies should be displayed.

    Returns:
        A rendered HTML page displaying the user's details and their associated movies.
    """
    user = next((u for u in data_manager.get_all_users() if u.id == user_id), None)
    if user is None:
        logger.warning(f"User with ID {user_id} not found.")
        flash(f"User with ID {user_id} not found.", 'error')
        return jsonify({'error': 'User not found', 'message': f'User with ID {user_id} not found.'}), 404

    try:
        movies = data_manager.get_movies_by_user(user_id)
        return render_template('movie_details.html', user=user, movies=movies)
    except Exception as e:
        logger.error(f"Error retrieving movies for user {user_id}: {e}")
        flash('An error occurred while loading movies.', 'error')
        return render_template('movie_details.html', user=user, movies=[])

@app.route('/user/<int:user_id>/movies', methods=['GET'])
def user_movies_json(user_id):
    """
    Returns the list of movies for a specific user in JSON format.
    """
    user = next((u for u in data_manager.get_all_users() if u.id == user_id), None)
    if user is None:
        logger.warning(f"User with ID {user_id} not found.")
        return jsonify({'error': 'User not found', 'message': f'User with ID {user_id} not found.'}), 404

    try:
        movies = data_manager.get_movies_by_user(user_id)
        movie_list = [{'name': movie.name, 'director': movie.director, 'year': movie.year, 'rating': movie.rating} for movie in movies]
        return jsonify({'user_id': user_id, 'movies': movie_list})
    except Exception as e:
        logger.error(f"Error retrieving movies for user {user_id}: {e}")
        return jsonify({'error': 'An error occurred while loading movies.'}), 500

@app.route('/add_movie/<int:user_id>', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Handles adding a new movie for a specific user.

    If the request method is POST, the movie's details are collected from the form and added to the database.
    On success, the user is redirected to their list of movies.
    For GET requests, it renders the 'add_movie.html' form.

    Parameters:
        user_id (int): The ID of the user to whom the movie will be added.

    Returns:
        - For GET requests: A rendered HTML page with a form for adding a movie.
        - For POST requests: A redirection to the 'user_movies' page for the user.
    """
    user = next((u for u in data_manager.get_all_users() if u.id == user_id), None)
    if user is None:
        logger.warning(f"User with ID {user_id} not found.")
        return jsonify({'error': 'User not found', 'message': f'User with ID {user_id} not found.'}), 404

    if request.method == 'POST':
        name = request.form.get('name')
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')

        # Validate form data
        if not name or not director or not year or not rating:
            return jsonify({'error': 'Validation failed', 'message': 'All fields are required.'}), 400

        try:
            year = int(year)
            rating = float(rating)
        except ValueError:
            return jsonify({'error': 'Invalid input', 'message': 'Invalid year or rating format.'}), 400

        try:
            data_manager.add_movie(name, director, year, rating, user_id)
            return jsonify({'success': True, 'message': 'Movie added successfully!'}), 200
        except Exception as e:
            logger.error(f"Error adding movie: {e}")
            return jsonify({'error': 'An error occurred', 'message': 'An error occurred while adding the movie.'}), 500

    return render_template('add_movie.html', user_id=user_id)

@app.route('/recommendations/<int:user_id>')
def recommendations(user_id):
    """
    Generates and displays movie recommendations for a specific user based on their favorite movies.

    This function fetches all movies for the user and sends the list of movie names to the OpenAI model for recommendations.
    The recommendations are then rendered on the 'recommendations.html' template.

    Parameters:
        user_id (int): The ID of the user for whom recommendations should be generated.

    Returns:
        A rendered HTML page displaying movie recommendations based on the user's favorite movies.
    """
    user = next((u for u in data_manager.get_all_users() if u.id == user_id), None)
    if user is None:
        logger.warning(f"User with ID {user_id} not found.")
        return jsonify({'error': 'User not found', 'message': f'User with ID {user_id} not found.'}), 404

    try:
        favorite_movies = [movie.name for movie in data_manager.get_movies_by_user(user_id)]
        recommendations = ai_features.get_movie_recommendations(favorite_movies)
        return render_template('recommendations.html', user=user, recommendations=recommendations)
    except Exception as e:
        logger.error(f"Error generating recommendations for user {user_id}: {e}")
        return jsonify({'error': 'An error occurred while generating recommendations.'}), 500

if __name__ == '__main__':
    """
    Runs the Flask application in debug mode.

    This is the entry point of the application, and it starts the Flask web server when the script is run directly.
    """
    app.run(host='0.0.0.0', port=5000, debug=True)
