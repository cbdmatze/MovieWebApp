from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from ai_features import AIFeatures

app = Flask(__name__)
data_manager = DataManager()
ai_features = AIFeatures()

@app.route('/')
def index():
    """
    Renders the homepage with a list of all users.

    This function retrieves all users from the DataManager and passes them to the 'index.html' template for display.

    Returns:
        A rendered HTML page displaying the list of users.
    """
    users = data_manager.get_all_users()
    return render_template('index.html', users=users)

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
    user = next(u for u in data_manager.get_all_users() if u.id == user_id)
    movies = data_manager.get_movies_by_user(user_id)
    return render_template('movie_details.html', user=user, movies=movies)

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
    if request.method == 'POST':
        name = request.form['name']
        director = request.form['director']
        year = int(request.form['year'])
        rating = float(request.form['rating'])
        data_manager.add_movie(name, director, year, rating, user_id)
        return redirect(url_for('user_movies', user_id=user_id))
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
    user = next(u for u in data_manager.get_all_users() if u.id == user_id)
    favorite_movies = [movie.name for movie in data_manager.get_movies_by_user(user_id)]
    recommendations = ai_features.get_movie_recommendations(favorite_movies)
    return render_template('recommendations.html', user=user, recommendations=recommendations)

if __name__ == '__main__':
    """
    Runs the Flask application in debug mode.

    This is the entry point of the application, and it starts the Flask web server when the script is run directly.
    """
    app.run(debug=True)
