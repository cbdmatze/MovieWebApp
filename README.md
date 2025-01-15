---

MovieWebApp 🎥

MovieWebApp is a Flask-based web application designed for users to manage and explore their favorite movies, add new entries, and receive AI-generated movie recommendations. The app integrates movie data management with OpenAI-powered features for recommendations, reviews, and trivia, all within a sleek, responsive interface styled using Tailwind CSS.



Key Features ✨

User Management: List, add, and update users.
Movie Collection: Users can add, view, and edit their favorite movies.
AI-Generated Recommendations: Receive personalized movie recommendations based on users' favorite movies.
Movie Reviews: Get AI-generated movie reviews and trivia.
Responsive Design: Stylish, responsive design using Tailwind CSS for optimal viewing on any device.




Technology Stack 🛠️

Backend: Flask
Frontend: HTML, Tailwind CSS
Database: SQLite
AI Features: OpenAI's GPT-3.5 (via openai Python package)




Prerequisites 📦

Python 3.8+
Virtual Environment (venv)
OpenAI API Key (set in the environment variables)
Installation & Setup 🚀
Clone the repository:



bash

git clone https://github.com/yourusername/MovieWebApp.git
cd MovieWebApp
Create and activate a virtual environment:



bash

python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install dependencies:



bash

pip install -r requirements.txt
Set up the environment variables: Ensure you have your OpenAI API key set up in your .env file:



makefile
OPENAI_API_KEY=your_openai_api_key
Run the app:



bash
python run.py
Access the app: Open your browser and go to http://127.0.0.1:5000/.





File Structure 🗂️

MOVIEWEBAPP/
├── .venv/                           # Virtual environment
├── .vscode/                         # VSCode settings
├── data/
│   ├── __init__.py                  # Init file for data module
│   ├── moviewebapp.db               # SQLite database
├── deploy/
│   ├── __init__.py                  # Init file for deploy module
│   ├── wsgi.py                      # WSGI entry point for deployment
├── static/
│   ├── __init__.py                  # Static module
│   ├── preview.html                 # Preview static HTML
│   └── style.css                    # Custom CSS styles for the app
├── super/                           # Virtual environment folder
│   ├── bin/
│   ├── include/
│   └── lib/
├── templates/
│   ├── __init__.py                  # Template module
│   ├── add_movie.html               # Template for adding a new movie
│   ├── base.html                    # Base template for the app
│   ├── edit_movie.html              # Template for editing movie details
│   ├── index.html                   # Homepage template
│   ├── movie_details.html           # Template for displaying movie details
│   ├── movie_list.html              # Template for listing movies
│   └── recommendations.html         # Template for AI movie recommendations
├── tests/
│   ├── __init__.py                  # Test module
│   ├── test_app.py                  # Unit tests for the Flask app
├── ai_features.py                   # AI features module (recommendations, reviews, trivia)
├── app.py                           # Flask application entry point
├── config.py                        # Configuration settings for the app
├── data_manager.py                  # Data management module (database access)
├── LICENSE                          # License information
├── README.md                        # Project documentation (this file)
├── requirements.txt                 # Python dependencies
├── run.py                           # Main script to run the Flask app
Screenshots 📸
Homepage (User List)




Add Movie Page




Tests 🧪
Run the test suite using:



bash
python -m unittest discover tests




Deployment 🚀

To deploy the application using WSGI, you can use the wsgi.py file located in the deploy/ folder. Here is a basic WSGI setup for deployment:



bash

gunicorn --workers 3 deploy.wsgi:app
License 📜
This project is licensed under the MIT License. See the LICENSE file for details.




Contributing 🤝

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.




Acknowledgements 🙏

Flask: For the amazing web framework.
Tailwind CSS: For making the app look sleek and responsive.
OpenAI GPT-3.5: For powering the AI features in this project.



Enjoy managing your movie collection and exploring new recommendations with MovieWebApp! 🍿🎬
