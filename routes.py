from flask import Flask, render_template, request , session , redirect , url_for , flash , jsonify
from models import db , User , Feedback , Movie , MovieInfo , WatchedMovies , WatchListMovies , FavMovies
from forms import SignupForm , LoginForm , FeedbackForm , SearchMovie 

app = Flask( __name__ )

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/learningflask"
db.init_app(app)

app.secret_key = "developement-key"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")	

@app.route("/signup" , methods=['GET', 'POST'])
def signup():
	if 'email' in session :
		return redirect(url_for('home'))

	form = SignupForm()

	if request.method == 'POST' :
		if form.validate() == False :
			return render_template('signup.html' , form=form)
		else :
			newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()
			
			session['email'] = newuser.email
			return redirect(url_for('home'))

	elif request.method == 'GET' :
	    return render_template('signup.html', form=form)

@app.route('/home' , methods=['GET', 'POST'])
def home():
	if 'email' not in session :
		return redirect(url_for('login'))

	form = SearchMovie()

	my_movie = []
	my_movie_dictExact = []

	if request.method == 'POST' :
		if form.validate() == False :
			return render_template("home.html" , form=form ,  moviename=my_movie , movienameExact=my_movie_dictExact)
		else :
			moviename = form.movie_name.data
			year = form.year.data

			m = Movie()
			my_movie_dictSearch = m.querySearch(moviename)
			my_movie_dictExact = m.queryExact(moviename , year)
			my_movie = my_movie_dictSearch.values()[0]
			return render_template('home.html', form=form , moviename=my_movie , movienameExact=my_movie_dictExact )
	
	elif request.method == 'GET' :
			return render_template("home.html" , form=form , moviename=my_movie , movienameExact=my_movie_dictExact)


@app.route('/_add_to_watched')
def add_watched():
	Title = request.args.get('Title')
	year = request.args.get('releaseYear')
	ImdbID = request.args.get('imdbID')
	Plot = request.args.get('Plot')
	Poster = request.args.get('Poster')
	actors = request.args.get('Actors')
	genre = request.args.get('Genre')
	itemtype = request.args.get('itemType')
	country = request.args.get('Country')
	awards = request.args.get('Awards')
	released = request.args.get('Released')
	writer = request.args.get('Writer')
	imdbvotes = request.args.get('imdbVotes')
	metascore = request.args.get('Metascore')
	runtime = request.args.get('Runtime')
	imdbrating = request.args.get('imdbRating')
	director = request.args.get('Director')
	language = request.args.get('Language')
	rated = request.args.get('Rated')

	mail=session['email']
	ed_User = User.query.filter_by(email=mail).first()
	currentuserid = ed_User.uid

	movieChk = MovieInfo.query.filter_by(imdbid=ImdbID).first()

	if (movieChk is not None)  :
		if (WatchedMovies.query.filter_by(user_id=currentuserid,movie_id=movieChk.id).first() is not None) :
			return jsonify(result='This movie is already watched')
		else :
			newMovieId = movieChk.id
			newWatchedMovie = WatchedMovies(currentuserid , newMovieId)
			db.session.add(newWatchedMovie)
			db.session.commit()
	else :
		newMovie = MovieInfo(ImdbID , Title , year , Plot , Poster , rated , released , runtime ,writer ,awards , country , metascore , imdbrating , imdbvotes , itemtype , genre , director , actors , language)
		db.session.add(newMovie)
		db.session.commit()

		newmovieChk = MovieInfo.query.filter_by(imdbid=ImdbID).first()
		newMovieId = newmovieChk.id

		newWatchedMovie = WatchedMovies(currentuserid , newMovieId)
		db.session.add(newWatchedMovie)
		db.session.commit()


@app.route('/_add_to_watchlist')
def add_watchlist():
	Title = request.args.get('Title')
	year = request.args.get('releaseYear')
	ImdbID = request.args.get('imdbID')
	Plot = request.args.get('Plot')
	Poster = request.args.get('Poster')
	actors = request.args.get('Actors')
	genre = request.args.get('Genre')
	itemtype = request.args.get('itemType')
	country = request.args.get('Country')
	awards = request.args.get('Awards')
	released = request.args.get('Released')
	writer = request.args.get('Writer')
	imdbvotes = request.args.get('imdbVotes')
	metascore = request.args.get('Metascore')
	runtime = request.args.get('Runtime')
	imdbrating = request.args.get('imdbRating')
	director = request.args.get('Director')
	language = request.args.get('Language')
	rated = request.args.get('Rated')

	mail=session['email']
	ed_User = User.query.filter_by(email=mail).first()
	currentuserid = ed_User.uid

	movieChk = MovieInfo.query.filter_by(imdbid=ImdbID).first()

	if movieChk is not None :
		if (WatchListMovies.query.filter_by(user_id=currentuserid,movie_id=movieChk.id).first() is not None) :
			return jsonify(result='movie is already added to watchlist')
		else :
			newMovieId = movieChk.id
			newWatchlistMovie = WatchListMovies(currentuserid , newMovieId)
			db.session.add(newWatchlistMovie)
			db.session.commit()
	else :
		newMovie = MovieInfo(ImdbID , Title , year , Plot , Poster , rated , released , runtime ,writer ,awards , country , metascore , imdbrating , imdbvotes , itemtype , genre , director , actors , language)
		db.session.add(newMovie)
		db.session.commit()

		newmovieChk = MovieInfo.query.filter_by(imdbid=ImdbID).first()
		newMovieId = newmovieChk.id

		newWatchListMovie = WatchListMovies(currentuserid , newMovieId)
		db.session.add(newWatchListMovie)
		db.session.commit()

@app.route('/_add_to_fav')
def add_fav():
	Title = request.args.get('Title')
	year = request.args.get('releaseYear')
	ImdbID = request.args.get('imdbID')
	Plot = request.args.get('Plot')
	Poster = request.args.get('Poster')
	actors = request.args.get('Actors')
	genre = request.args.get('Genre')
	itemtype = request.args.get('itemType')
	country = request.args.get('Country')
	awards = request.args.get('Awards')
	released = request.args.get('Released')
	writer = request.args.get('Writer')
	imdbvotes = request.args.get('imdbVotes')
	metascore = request.args.get('Metascore')
	runtime = request.args.get('Runtime')
	imdbrating = request.args.get('imdbRating')
	director = request.args.get('Director')
	language = request.args.get('Language')
	rated = request.args.get('Rated')

	mail=session['email']
	ed_User = User.query.filter_by(email=mail).first()
	currentuserid = ed_User.uid

	movieChk = MovieInfo.query.filter_by(imdbid=ImdbID).first()

	if movieChk is not None :
		if (FavMovies.query.filter_by(user_id=currentuserid,movie_id=movieChk.id).first() is not None) :
			return jsonify(result='movie already added to Fav')
		else :
			if (WatchedMovies.query.filter_by(user_id=currentuserid,movie_id=movieChk.id).first() is not None) :
				newMovieId = movieChk.id
				newFavMovie = FavMovies(currentuserid , newMovieId)
				db.session.add(newFavMovie)
				db.session.commit()
				return jsonify(result='movie already added to Watched so only added to Fav')
			else :	
				newMovieId = movieChk.id
				newFavMovie = FavMovies(currentuserid , newMovieId)
				newWatchedMovie = WatchedMovies(currentuserid,newMovieId)
				db.session.add(newFavMovie)
				db.session.add(newWatchedMovie)
				db.session.commit()
	else :
		newMovie = MovieInfo(ImdbID , Title , year , Plot , Poster , rated , released , runtime ,writer ,awards , country , metascore , imdbrating , imdbvotes , itemtype , genre , director , actors , language)
		db.session.add(newMovie)
		db.session.commit()

		newmovieChk = MovieInfo.query.filter_by(imdbid=ImdbID).first()
		newMovieId = newmovieChk.id

		newFavMovie = FavMovies(currentuserid , newMovieId)
		newWatchedMovie = WatchedMovies(currentuserid,newMovieId)
		db.session.add(newFavMovie)
		db.session.add(newWatchedMovie)
		db.session.commit()    

@app.route("/_moved_to_Fav")
def moved_to_Fav():
	newMovieIdToFav = request.args.get('id')

	mail=session['email']
	ed_User = User.query.filter_by(email=mail).first()
	currentuserid = ed_User.uid
	if (FavMovies.query.filter_by(user_id=currentuserid,movie_id=newMovieIdToFav).first() is not None) :
			return jsonify(result='movie already added to Fav')
	else :
			newFavMovie = FavMovies(currentuserid , newMovieIdToFav)
			db.session.add(newFavMovie)
			db.session.commit()

@app.route("/watched")
def watched():
	if 'email' not in session :
		return redirect(url_for('login'))
	
	else:
		mail=session['email']
		ed_User = User.query.filter_by(email=mail).first()
		currentuserid = ed_User.uid
		watchedMovies = WatchedMovies.query.join(MovieInfo, WatchedMovies.movie_id==MovieInfo.id).add_columns(MovieInfo.poster, MovieInfo.title, MovieInfo.year,  MovieInfo.itemtype , MovieInfo.id).filter(WatchedMovies.movie_id==MovieInfo.id).filter(WatchedMovies.user_id == currentuserid)
		return render_template("watched.html" , watchedMovies = watchedMovies)


@app.route("/watchlist")
def watchlist():
	if 'email' not in session :
		return redirect(url_for('login'))
	
	else:
		mail=session['email']
		ed_User = User.query.filter_by(email=mail).first()
		currentuserid = ed_User.uid
		myWatchListMovies = WatchListMovies.query.join(MovieInfo, WatchListMovies.movie_id==MovieInfo.id).add_columns(MovieInfo.poster, MovieInfo.title, MovieInfo.year , MovieInfo.itemtype).filter(WatchListMovies.movie_id==MovieInfo.id).filter(WatchListMovies.user_id == currentuserid)
		return render_template("watchlist.html" , myWatchListMovies = myWatchListMovies)


@app.route("/fav")
def fav():
	if 'email' not in session :
		return redirect(url_for('login'))
	
	else:
		mail=session['email']
		ed_User = User.query.filter_by(email=mail).first()
		currentuserid = ed_User.uid
		myFavMovies = FavMovies.query.join(MovieInfo, FavMovies.movie_id==MovieInfo.id).add_columns(MovieInfo.poster, MovieInfo.title, MovieInfo.year , MovieInfo.itemtype).filter(FavMovies.movie_id==MovieInfo.id).filter(FavMovies.user_id == currentuserid)
		return render_template("favlist.html" , myFavMovies = myFavMovies)


@app.route('/feedback' , methods=['GET','POST'])
def feedback():
	if 'email' not in session :
		return redirect(url_for('login'))

	form = FeedbackForm()

	if request.method == 'POST' :
		if form.validate() == False :
			return render_template("feedback.html" , form=form)
		else :
			newfeedback = Feedback(form.first_name.data , form.email.data , form.comments.data)
			db.session.add(newfeedback)
			db.session.commit()
			return redirect(url_for('home'))

	elif request.method == 'GET' :
		return render_template("feedback.html" , form=form)


@app.route("/login" , methods=['GET','POST'])
def login():
	if 'email' in session :
		return redirect(url_for('home'))

	form = LoginForm()

	if request.method == 'POST' :
		if form.validate() == False :
			return render_template('login.html' , form=form)
		else :
			email = form.email.data
			password = form.password.data

			user = User.query.filter_by(email=email).first()
			if user is not None and user.check_password(password) :
				session['email'] = form.email.data
				return redirect(url_for('home'))
			else :
				return redirect(url_for('login'))

	elif request.method == 'GET' :
		return render_template("login.html" , form=form)

@app.route('/logout')
def logout():
	session.pop('email' , None)
	return redirect(url_for('index'))

if __name__ == "__main__" :
	app.run(debug=True)
