import openai
import os

class AIFeatures:
    def __init__(self):
        """
        Initializes the AIFeatures class by setting up the OpenAI API key.
        The API key is retrieved from an environment variable 'OPENAI_API_KEY'.
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def get_movie_recommendations(self, favorite_movies):
        """
        Generates movie recommendations based on a list of favorite movies.

        Parameters:
            favorite_movies (list): A list of strings representing the user's favorite movies.

        Returns:
            str: A text response with recommended movies based on the user's favorites.
        """
        prompt = f"Recommend movies based on the following favorites: {', '.join(favorite_movies)}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a movie recommendation assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']

    def generate_movie_review(self, movie_name):
        """
        Generates a brief movie review based on the given movie name.

        Parameters:
            movie_name (str): The name of the movie to generate a review for.

        Returns:
            str: A brief review of the specified movie.
        """
        prompt = f"Write a brief movie review for {movie_name}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a movie reviewer."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']

    def get_movie_trivia(self, movie_name):
        """
        Provides an interesting piece of trivia about a specific movie.

        Parameters:
            movie_name (str): The name of the movie to get trivia for.

        Returns:
            str: A trivia fact about the specified movie.
        """
        prompt = f"Give me an interesting trivia about the movie {movie_name}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a movie trivia expert."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
