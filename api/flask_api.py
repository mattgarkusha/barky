from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import services.commands

# init from dotenv file
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

class FlaskBookmarkAPI(AbstractBookMarkAPI):
    """
    Flask 
    """
    def __init__(self) -> None:
        super().__init__()
    
    @app.route('/')
    def index(self):
        return f'Barky API'

    @app.route('/api/all')
    def all(self):
        return services.commands.ListBookmarksCommand.execute()
    
    def add(bookmark):
        return services.commands.AddBookmarkCommand.execute(bookmark)

    def delete(bookmark):
        return services.commands.DeleteBookmarkCommand.execute(bookmark)

    def update(bookmark):
        return services.commands.EditBookmarkCommand.execute(bookmark)