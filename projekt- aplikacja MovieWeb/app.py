
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Tworzenie instancji bazy danych
engine = create_engine('sqlite:///movies.db', echo=True)
Base = declarative_base()

# Definicja modelu danych
class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)
    rating = Column(Float)

# Tworzenie bazy danych
Base.metadata.create_all(engine)

# Tworzenie sesji
Session = sessionmaker(bind=engine)
session = Session()

# Funkcje operacji CRUD
@app.route('/')
def index():
    movies = session.query(Movie).all()
    return render_template('index.html', movies=movies)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    movies = session.query(Movie).filter(
        (Movie.title.like(f"%{query}%")) |
        (Movie.genre.like(f"%{query}%"))
    ).all()
    return render_template('index.html', movies=movies)

@app.route('/filter', methods=['POST'])
def filter():
    sort_by = request.form['sort_by']
    if sort_by == 'title':
        movies = session.query(Movie).order_by(Movie.title).all()
    elif sort_by == 'genre':
        movies = session.query(Movie).order_by(Movie.genre).all()
    elif sort_by == 'rating':
        movies = session.query(Movie).order_by(Movie.rating).all()
    return render_template('index.html', movies=movies)

@app.route('/add_movie', methods=['POST'])
def add_movie():
    title = request.form['title']
    genre = request.form['genre']
    rating = float(request.form['rating'])
    movie = Movie(title=title, genre=genre, rating=rating)
    session.add(movie)
    session.commit()
    return redirect(url_for('index'))

@app.route('/delete_movie/<int:movie_id>')
def delete_movie(movie_id):
    movie = session.query(Movie).filter_by(id=movie_id).first()
    session.delete(movie)
    session.commit()
    return redirect(url_for('index'))

@app.route('/edit_movie/<int:movie_id>')
def edit_movie(movie_id):
    movie = session.query(Movie).filter_by(id=movie_id).first()
    return render_template('edit_movie.html', movie=movie)

@app.route('/update_movie/<int:movie_id>', methods=['POST'])
def update_movie(movie_id):
    movie = session.query(Movie).filter_by(id=movie_id).first()
    movie.title = request.form['title']
    movie.genre = request.form['genre']
    movie.rating = float(request.form['rating'])
    session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
