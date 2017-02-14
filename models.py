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


class Movie(object):
  def query(self,moviename) :
    query_url = 'http://netflixroulette.net/api/api.php?title=' + moviename
    m = urllib2.urlopen(query_url)
    movielist = m.read()
    m.close()

    data = json.loads(movielist)
    
    """title = data['show_title']
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
    }"""



    return data