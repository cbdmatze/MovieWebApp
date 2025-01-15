import sqlite3

class DataManager:
    def __init__(self):
        """
        Initializes the DataManager class and sets the database file location.
        Automatically calls the create_tables method to ensure tables exist.
        """
        self.db_file = 'data/moviweb.db'
        self.create_tables()

    def create_tables(self):
        """
        Creates the 'users' and 'movies' tables in the database if they do not already exist.
        'users' table stores basic user information.
        'movies' table stores movie information linked to users via foreign key.
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Create Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')

        # Create Movies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                director TEXT,
                year INTEGER,
                rating REAL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.commit()
        conn.close()

    def get_all_users(self):
        """
        Retrieves all users from the 'users' table.

        Returns:
            list: A list of User objects representing each user in the 'users' table.
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        conn.close()
        return [User(id=user[0], name=user[1]) for user in users]

    def get_movies_by_user(self, user_id):
        """
        Retrieves all movies associated with a specific user.

        Parameters:
            user_id (int): The ID of the user whose movies are to be retrieved.

        Returns:
            list: A list of Movie objects for each movie associated with the given user_id.
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movies WHERE user_id = ?', (user_id,))
        movies = cursor.fetchall()
        conn.close()
        return [Movie(id=movie[0], name=movie[1], director=movie[2], year=movie[3], rating=movie[4], user_id=movie[5]) for movie in movies]

    def add_movie(self, name, director, year, rating, user_id):
        """
        Adds a new movie to the 'movies' table.

        Parameters:
            name (str): The name of the movie.
            director (str): The director of the movie.
            year (int): The release year of the movie.
            rating (float): The rating of the movie.
            user_id (int): The ID of the user who owns the movie.

        Returns:
            None
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO movies (name, director, year, rating, user_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, director, year, rating, user_id))
        conn.commit()
        conn.close()

    def delete_movie(self, movie_id):
        """
        Deletes a movie from the 'movies' table based on its ID.

        Parameters:
            movie_id (int): The ID of the movie to be deleted.

        Returns:
            None
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
        conn.commit()
        conn.close()

    def update_movie(self, movie_id, name, director, year, rating):
        """
        Updates the details of a movie in the 'movies' table based on its ID.

        Parameters:
            movie_id (int): The ID of the movie to be updated.
            name (str): The new name of the movie.
            director (str): The new director of the movie.
            year (int): The new release year of the movie.
            rating (float): The new rating of the movie.

        Returns:
            None
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE movies
            SET name = ?, director = ?, year = ?, rating = ?
            WHERE id = ?
        ''', (name, director, year, rating, movie_id))
        conn.commit()
        conn.close()

class User:
    def __init__(self, id, name):
        """
        Represents a user in the system.

        Parameters:
            id (int): The ID of the user.
            name (str): The name of the user.
        """
        self.id = id
        self.name = name

class Movie:
    def __init__(self, id, name, director, year, rating, user_id):
        """
        Represents a movie in the system.

        Parameters:
            id (int): The ID of the movie.
            name (str): The name of the movie.
            director (str): The director of the movie.
            year (int): The release year of the movie.
            rating (float): The rating of the movie.
            user_id (int): The ID of the user who owns the movie.
        """
        self.id = id
        self.name = name
        self.director = director
        self.year = year
        self.rating = rating
        self.user_id = user_id
