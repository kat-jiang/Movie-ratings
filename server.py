"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!
@app.route("/")
def homepage():
    """View homepage"""
    return render_template("homepage.html")

@app.route("/movies")
def view_all_movies():
    """View all movies"""

    movies = crud.all_movie()

    return render_template("all_movies.html", movies= movies)

@app.route("/movies/<movie_id>")
def movie_detail(movie_id):
    """Show details on movie's page"""
    
    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route("/users")
def show_all_users():
    """View all users"""
    
    users = crud.get_all_user()
    
    return render_template("all_users.html",users = users)

@app.route("/users/<user_id>")
def user_profile(user_id):
    """View user's profiles"""

    user = crud.get_user_by_id(user_id)

    return render_template("user_profile.html",user = user)

@app.route("/register", methods=["POST"])
def register():
    """Check if email exist. If not will allow user to register their email."""
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    
    if user is None:
        new_user = crud.create_user(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash("The account was created successfully!")
    else: 
        flash("You can't create an account with that email, please try again!") 
    
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    """User login"""
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user.password == password: 
        session['user'] = user.email
        flash(f"Welcome back, {user.email}!")
    else: 
        flash("Sorry, passwords do not match!")

    return redirect("/")

@app.route("/movies/<movie_id>/ratings", methods=["POST"])
def add_movie_rating(movie_id):
    """Add a movie rating"""

    movie_rating = request.form.get("mv_rating")
    current_useremail = session.get('user')
    
    if current_useremail is None:
        flash("You must log in to rate a movie.")
    elif not movie_rating:
        flash("Error: you didn't select a score for your rating.")
    else:
        
        movie = crud.get_movie_by_id(movie_id)
        current_user = crud.get_user_by_email(current_useremail)

        new_rating = crud.create_rating(movie_rating, movie, current_user)
        db.session.add(new_rating)
        db.session.commit()

    return redirect(f'/movies/{movie_id}')

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
