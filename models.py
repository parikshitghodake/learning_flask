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
  title = db.Column(db.String(200))
  year = db.Column(db.String(20))
  plot = db.Column(db.String(3000))
  poster = db.Column(db.String(500))
  rated = db.Column(db.String(20))
  released = db.Column(db.String(50))
  runtime = db.Column(db.String(50))
  writer = db.Column(db.String(1000))
  awards = db.Column(db.String(900))
  country = db.Column(db.String(50))
  metascore = db.Column(db.String(50))
  imdbrating = db.Column(db.String(50))
  imdbvotes = db.Column(db.String(50))
  itemtype = db.Column(db.String(50))
  genre = db.Column(db.String(500))
  director = db.Column(db.String(500))
  actors = db.Column(db.String(1000))
  language = db.Column(db.String(500))
  tomatometer = db.Column(db.String(200))
  tomatorating = db.Column(db.String(200))
  tomatousermeter = db.Column(db.String(200))
  tomatouserrating = db.Column(db.String(200))
  tomatourl = db.Column(db.String(500))
  dvd = db.Column(db.String(200))
  boxoffice = db.Column(db.String(200))
  production = db.Column(db.String(500))
  website = db.Column(db.String(500))
  imdbscores = db.Column(db.String(200))
  rtscores = db.Column(db.String(200))
  metascores = db.Column(db.String(200))
  def __init__(self, imdbid, title, year , plot , poster ,rated , released , runtime ,writer ,awards , country , metascore , imdbrating , imdbvotes , itemtype , genre , director , actors , language , tomatometer , tomatorating, tomatousermeter, tomatouserrating, tomatourl, dvd, boxoffice, production, website, imdbscores, rtscores, metascores):
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
    self.tomatometer = tomatometer
    self.tomatorating = tomatorating
    self.tomatousermeter = tomatousermeter
    self.tomatouserrating = tomatouserrating
    self.tomatourl = tomatourl
    self.dvd = dvd
    self.boxoffice = boxoffice
    self.production = production
    self.website = website
    self.imdbscores = imdbscores
    self.rtscores = rtscores
    self.metascores = metascores

class WatchedMovies(db.Model):
    __tablename__ = 'watchedmoviesfact'
    watchedmovies_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    movie_id = db.Column(db.Integer)
    # isfav = db.Column(db.Boolean, default=False)
    # addedon = db.Column(db.Date)

    def __init__(self, user_id, movie_id):
      self.user_id = user_id
      self.movie_id = movie_id
      # self.isfav = isfav
      # self.addedon = addedon
      
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
    query_url = 'http://www.omdbapi.com/?t=' + moviename + '&y=' + year + '&tomatoes=true'
    m = urllib2.urlopen(query_url)
    movielist = m.read()
    m.close()

    movienameExact = json.loads(movielist)
    

    imdbRatings = 'N/A'
    rtRatings = 'N/A'
    metaRatings = 'N/A'
    try :
        for value in movienameExact['Ratings'] :
            if value['Source'] == 'Internet Movie Database' :
               imdbRatings = value['Value']
            elif value['Source'] == 'Rotten Tomatoes' :
               rtRatings = value['Value']
            elif value['Source'] == 'Metacritic' :
               metaRatings = value['Value']
    except :
        imdbRatings = 'N/A'
        rtRatings = 'N/A'
        metaRatings = 'N/A'        

    Title = movienameExact['Title']
    Year = movienameExact['Year']
    imdbID = movienameExact['imdbID']
    Plot = movienameExact['Plot']
    Poster = movienameExact['Poster']
    Actors = movienameExact['Actors']
    Genre = movienameExact['Genre']
    Type = movienameExact['Type']
    Country = movienameExact['Country']
    Awards = movienameExact['Awards']
    Released = movienameExact['Released']
    Writer = movienameExact['Writer']
    imdbVotes = movienameExact['imdbVotes']
    Metascore = movienameExact['Metascore']
    Runtime = movienameExact['Runtime']
    imdbRating = movienameExact['imdbRating']
    Director = movienameExact['Director']
    Language = movienameExact['Language']
    Rated = movienameExact['Rated']
    tomatoMeter = movienameExact['tomatoMeter']
    tomatoRating = movienameExact['tomatoRating']
    tomatoUserMeter = movienameExact['tomatoUserMeter']
    tomatoUserRating = movienameExact['tomatoUserRating']
    tomatoURL = movienameExact['tomatoURL']
    DVD = movienameExact['DVD']
    BoxOffice = movienameExact['BoxOffice']
    Production = movienameExact['Production']
    Website = movienameExact['Website']
    imdbScore = imdbRatings
    rtScore = rtRatings
    metaScore = metaRatings



    movieobj = {
    'Title' : Title ,
    'Year' : Year ,
    'imdbID' : imdbID ,
    'Plot' : Plot ,
    'Poster' : Poster ,
    'Actors' : Actors ,
    'Genre' : Genre ,
    'Type' : Type ,
    'Country' : Country ,
    'Awards' : Awards ,
    'Released' : Released ,
    'Writer' : Writer ,
    'imdbVotes' : imdbVotes ,
    'Metascore' : Metascore ,
    'Runtime' : Runtime ,
    'imdbRating' : imdbRating ,
    'Director' : Director ,
    'Language' : Language ,
    'Rated' : Rated ,
    'tomatoMeter' : tomatoMeter,
    'tomatoRating' : tomatoRating,
    'tomatoUserMeter' : tomatoUserMeter,
    'tomatoUserRating' : tomatoUserRating,
    'tomatoURL' : tomatoURL,
    'DVD' : DVD,
    'BoxOffice' : BoxOffice,
    'Production' : Production,
    'Website' : Website,
    'imdbScore' : imdbScore,
    'rtScore' : rtScore,
    'metaScore' : metaScore
    }
    return movieobj 