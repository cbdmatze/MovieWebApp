import sqlite3


class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Movie:
    def __init__(self, id, name, director, year, rating, user_id):
        self.id = id
        self.name = name
        self.director = director
        self.year = year
        self.rating = rating
        self.user_id = user_id


class DataManager:
    def __init__(self):
        self.db_file = 'data/moviewebapp.db'
        self.create_tables()

    def create_tables(self):
        try:
            with sqlite3.connect(self.db_file) as conn:
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
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def add_user(self, name):
        """
        Adds a new user to the 'users' table.

        Parameters:
            name (str): The name of the user.

        Returns:
            None
        """
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (name)
                    VALUES (?)
                ''', (name,))
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")

    def get_all_users(self):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users')
                users = cursor.fetchall()
            return [User(id=user[0], name=user[1]) for user in users]
        except sqlite3.Error as e:
            print(f"Error retrieving users: {e}")
            return []

    def get_movies_by_user(self, user_id):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM movies WHERE user_id = ?', (user_id,))
                movies = cursor.fetchall()
            return [Movie(id=movie[0], name=movie[1], director=movie[2], year=movie[3], rating=movie[4], user_id=movie[5]) for movie in movies]
        except sqlite3.Error as e:
            print(f"Error retrieving movies for user {user_id}: {e}")
            return []

    def add_movie(self, name, director, year, rating, user_id):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO movies (name, director, year, rating, user_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, director, year, rating, user_id))
        except sqlite3.Error as e:
            print(f"Error adding movie: {e}")

    def delete_movie(self, movie_id):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
        except sqlite3.Error as e:
            print(f"Error deleting movie with ID {movie_id}: {e}")

    def update_movie(self, movie_id, name, director, year, rating):
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE movies
                    SET name = ?, director = ?, year = ?, rating = ?
                    WHERE id = ?
                ''', (name, director, year, rating, movie_id))
        except sqlite3.Error as e:
            print(f"Error updating movie with ID {movie_id}: {e}")
