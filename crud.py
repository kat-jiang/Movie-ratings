"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie= Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)

    return movie

def create_rating(score, movie, user):
    """Create and return a rating"""

    rating = Rating(score=score, movie = movie, user=user)

    return rating

def all_movie():
    """Return all movies"""

    return Movie.query.all()

def get_movie_by_id(movie_id):
    """Return movie info by movie_id"""
    # Movie.query.get(movie_id)
    return Movie.query.filter_by(movie_id=movie_id).one()

def get_all_user():
    """Return all users"""

    return User.query.all()

def get_user_by_id(user_id):
    """Return user info by user_id"""
    
    return User.query.get(user_id)

def get_user_by_email(user_email):
    """Return user email if it exists, else returns None """

    return User.query.filter_by(email = user_email).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)