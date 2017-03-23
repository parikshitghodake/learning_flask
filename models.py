from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

import urllib2
import json

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))

  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)


class Feedback(db.Model):
  __tablename__ = 'feedback'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  email = db.Column(db.String(120))
  comments = db.Column(db.String(500))

  def __init__(self, firstname, email, comments):
    self.firstname = firstname.title()
    self.email = email.lower()
    self.comments = comments.title()

class MovieInfo(db.Model):
  __tablename__ = 'moviedim'
  id = db.Column(db.Integer, primary_key = True)
  imdbid = db.Column(db.String(50), unique=True)
  title = db.Column(db.String(100))
  year = db.Column(db.String(20))
  plot = db.Column(db.String(1000))
  poster = db.Column(db.String(300))
  rated = db.Column(db.String(20))
  released = db.Column(db.String(20))
  runtime = db.Column(db.String(20))
  writer = db.Column(db.String(200))
  awards = db.Column(db.String(300))
  country = db.Column(db.String(50))
  metascore = db.Column(db.String(10))
  imdbrating = db.Column(db.String(10))
  imdbvotes = db.Column(db.String(20))
  itemtype = db.Column(db.String(20))
  genre = db.Column(db.String(100))
  director = db.Column(db.String(100))
  actors = db.Column(db.String(200))
  language = db.Column(db.String(200))

  def __init__(self, imdbid, title, year , plot , poster ,rated , released , runtime ,writer ,awards , country , metascore , imdbrating , imdbvotes , itemtype , genre , director , actors , language):
    self.imdbid = imdbid
    self.title = title
    self.year = year
    self.plot = plot
    self.poster = poster
    self.rated  = rated   
    self.released = released
    self.runtime = runtime
    self.writer = writer
    self.awards = awards
    self.country = country
    self.metascore = metascore
    self.imdbrating = imdbrating
    self.imdbvotes = imdbvotes
    self.itemtype = itemtype
    self.genre = genre
    self.director = director
    self.actors = actors
    self.language = language

class WatchedMovies(db.Model):
    __tablename__ = 'watchedmoviesfact'
    watchedmovies_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    movie_id = db.Column(db.Integer)
    #watched_date = db.Column(db.Column(date))

    def __init__(self, user_id, movie_id):
      self.user_id = user_id
      self.movie_id = movie_id
      #self.watched_date = CURRENT_DATE
      
class WatchListMovies(db.Model):
    __tablename__ = 'watchlistmoviesfact'
    watchlistmovies_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    movie_id = db.Column(db.Integer)
    #watched_date = db.Column(db.Column(date))

    def __init__(self, user_id, movie_id):
      self.user_id = user_id
      self.movie_id = movie_id
      #self.watched_date = CURRENT_DATE

class FavMovies(db.Model):
    __tablename__ = 'favmoviesfact'
    favmovies_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    movie_id = db.Column(db.Integer)
    #watched_date = db.Column(db.Column(date))

    def __init__(self, user_id, movie_id):
      self.user_id = user_id
      self.movie_id = movie_id
      #self.watched_date = CURRENT_DATE      

class Movie(object):
  def querySearch(self,moviename) :
    moviename = "+".join(moviename.split())
    query_url = 'http://www.omdbapi.com/?s=' + moviename
    m = urllib2.urlopen(query_url)
    movielist = m.read()
    m.close()

    data = json.loads(movielist)
    return data

  def queryExact(self,moviename ,year) :
    year = year
    moviename = "+".join(moviename.split())
    query_url = 'http://www.omdbapi.com/?t=' + moviename + '&y=' + year
    m = urllib2.urlopen(query_url)
    movielist = m.read()
    m.close()

    data = json.loads(movielist)
    '''
    title = data['show_title']
    category = data['category']
    year = data['release_year']
    poster = data['poster']
    cast = data['show_cast']
    summary = data['summary']
    director = data['director']
    runtime = data['runtime']

    movieobj = {
    'title' : title,
    'category' : category,
    'year' : year,
    'poster':poster,
    'director':director,
    'summary':summary,
    'cast':cast
    }'''
    return data  