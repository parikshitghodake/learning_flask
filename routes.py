from flask import Flask, render_template, request , session , redirect , url_for , flash , jsonify
from models import db , User , Feedback , Movie , MovieInfo , WatchedMovies , WatchListMovies , FavMovies
from forms import SignupForm , LoginForm , FeedbackForm , SearchMovie 

app = Flask( __name__ )

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/learningflask"
db.init_app(app)

app.secret_key = "developement-key"

#Go to index page
@app.route("/")
def index():
	return render_template("index.html")

#Go to about page
@app.route("/about")
def about():
	return render_template("about.html")	

#Go to sign up page
@app.route("/signup" , methods=['GET', 'POST'])
def signup():
	#Check if session has email in it , if user is logged in  redirect to home page directly
	if 'email' in session :
		return redirect(url_for('home'))

	# if user is not logged in and clicked on sign up redirect to sign up page
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


#Go to Home page
@app.route('/home' , methods=['GET', 'POST'])
def home():
	# if user is not logged in redirect to log in page
	if 'email' not in session :
		return redirect(url_for('login'))

	# if user is is logged in rdirect to home page 	
	form = SearchMovie()

	my_movie = []
	my_movie_dictExact = []

	#when search button is clicked 
	if request.method == 'POST' :
		# if form validation fails , show error and redirect to home page again
		if form.validate() == False :
			return render_template("home.html" , form=form ,  moviename=my_movie , movienameExact=my_movie_dictExact)

		else :
			#get entered movie name and its year 
			moviename = form.movie_name.data
			year = form.year.data

			#pass it to Movie model to get exact movie and search result
			m = Movie()
			my_movie_dictSearch = m.querySearch(moviename)
			my_movie_dictExact = m.queryExact(moviename , year)
			#dict value 0 will return movies dictionary
			my_movie = my_movie_dictSearch.values()[0]
			# render result on home page
			return render_template('home.html', form=form , moviename=my_movie , movienameExact=my_movie_dictExact )
	
	elif request.method == 'GET' :
			return render_template("home.html" , form=form , moviename=my_movie , movienameExact=my_movie_dictExact)


# On click on WATCHED button on search result
@app.route('/_add_to_watched')
def add_watched():
	# Get JSON object into variables
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

	#Get logged in user id 
	mail=session['email']
	ed_User = User.query.filter_by(email=mail).first()
	currentuserid = ed_User.uid
	#Check if this movie exists in MovieDim
	movieChk = MovieInfo.query.filter_by(imdbid=ImdbID).first()
	# if Movie is present in MovieDim
	if (movieChk is not None)  :
		#If movie is already added to watched movies
		if (WatchedMovies.query.filter_by(user_id=currentuserid,movie_id=movieChk.id).first() is not None) :
			return jsonify(result='This movie is already watched')
		else :
			# if movie is not added to watched movies then add current user id and movie id from moviedim
			newMovieId = movieChk.id
			newWatchedMovie = WatchedMovies(currentuserid , newMovieId)
			db.session.add(newWatchedMovie)
			db.session.commit()
	else :
		# If movie is not added to moviedim , then add movie to MovieDim 
		newMovie = MovieInfo(ImdbID , Title , year , Plot , Poster , rated , released , runtime ,writer ,awards , country , metascore , imdbrating , imdbvotes , itemtype , genre , director , actors , language)
		db.session.add(newMovie)
		db.session.commit()
		# Get id of newly added movie from MovieDim , 
		newmovieChk = MovieInfo.query.filter_by(imdbid=ImdbID).first()
		newMovieId = newmovieChk.id
		#Add newly added movie id and current user to watched list 
		newWatchedMovie = WatchedMovies(currentuserid , newMovieId)
		db.session.add(newWatchedMovie)
		db.session.commit()

# On click on WATCH LIST button on search result
@app.route('/_add_to_watchlist')
def add_watchlist():
	# Get JSON object into variables
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

	#Get logged in user id 
	mail=session['email']
	ed_User = User.query.filter_by(email=mail).first()
	currentuserid = ed_User.uid
	#Check if this movie exists in MovieDim
	movieChk = MovieInfo.query.filter_by(imdbid=ImdbID).first()

	# if Movie is present in MovieDim
	if movieChk is not None :
		#If movie is already added to watchList movies
		if (WatchListMovies.query.filter_by(user_id=currentuserid,movie_id=movieChk.id).first() is not None) :
			return jsonify(result='movie is already added to watchlist')
		else :
			# if movie is not added to watchList movies then add current user id and movie id from moviedim
			newMovieId = movieChk.id
			newWatchlistMovie = WatchListMovies(currentuserid , newMovieId)
			db.session.add(newWatchlistMovie)
			db.session.commit()
	else :
		# If movie is not added to moviedim , then add movie to MovieDim 
		newMovie = MovieInfo(ImdbID , Title , year , Plot , Poster , rated , released , runtime ,writer ,awards , country , metascore , imdbrating , imdbvotes , itemtype , genre , director , actors , language)
		db.session.add(newMovie)
		db.session.commit()
		# Get id of newly added movie from MovieDim , 
		newmovieChk = MovieInfo.query.filter_by(imdbid=ImdbID).first()
		newMovieId = newmovieChk.id
		#Add newly added movie id and current user to watchList list 
		newWatchListMovie = WatchListMovies(currentuserid , newMovieId)
		db.session.add(newWatchListMovie)
		db.session.commit()

# On click on Favorite button on search result
@app.route('/_add_to_fav')
def add_fav():
	#Get JSON obejct to variables
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

	#Get current user id
	mail=session['email']
	ed_User = User.query.filter_by(email=mail).first()
	currentuserid = ed_User.uid

	#Check if movie present in MovieDim
	movieChk = MovieInfo.query.filter_by(imdbid=ImdbID).first()
	#If movie is present in MOvie Dim
	if movieChk is not None :
		#If Movie is already added to Favorite list
		if (FavMovies.query.filter_by(user_id=currentuserid,movie_id=movieChk.id).first() is not None) :
			return jsonify(result='movie already added to Fav')
		else :
			# Check if Movie is in Watched movie as Fav movie has to watched before
			if (WatchedMovies.query.filter_by(user_id=currentuserid,movie_id=movieChk.id).first() is not None) :
				#If movie is already to Watched movies list then add only to Favorite list
				newMovieId = movieChk.id
				newFavMovie = FavMovies(currentuserid , newMovieId)
				db.session.add(newFavMovie)
				db.session.commit()
				return jsonify(result='movie already added to Watched so only added to Fav')
			else :	
				# If movie is not added to Watched Movies , then first add to Watched movies then add to Favorite movie list
				newMovieId = movieChk.id
				newFavMovie = FavMovies(currentuserid , newMovieId)
				newWatchedMovie = WatchedMovies(currentuserid,newMovieId)
				db.session.add(newFavMovie)
				db.session.add(newWatchedMovie)
				db.session.commit()
	else :
		#If movie is not there in MovieDim , Add movie to Movie Dim first
		newMovie = MovieInfo(ImdbID , Title , year , Plot , Poster , rated , released , runtime ,writer ,awards , country , metascore , imdbrating , imdbvotes , itemtype , genre , director , actors , language)
		db.session.add(newMovie)
		db.session.commit()

		# Get Id of newly added movie
		newmovieChk = MovieInfo.query.filter_by(imdbid=ImdbID).first()
		newMovieId = newmovieChk.id
		# Add newly added movie from MovieDim to Watched as well as Fav Movies
		newFavMovie = FavMovies(currentuserid , newMovieId)
		newWatchedMovie = WatchedMovies(currentuserid,newMovieId)
		db.session.add(newFavMovie)
		db.session.add(newWatchedMovie)
		db.session.commit()    


#Add movie to Fav movies from Watched Movie page , on click of Fav button below every movie of Watched Page
@app.route("/_moved_to_Watched")
def moved_to_Watched():
	# Get id of movie from page to add to fav
	newMovieIdToFav = request.args.get('id')

	#Get id of current user
	mail=session['email']
	ed_User = User.query.filter_by(email=mail).first()
	currentuserid = ed_User.uid
	# if Movie is already added to Fav show message it is already added
	if (WatchedMovies.query.filter_by(user_id=currentuserid,movie_id=newMovieIdToFav).first() is not None) :
			return jsonify(result='movie already added to Fav')
	else :
			#if movie is not in Favorite list add this movie to Favorite movies list		
			newFavMovie = WatchedMovies(currentuserid , newMovieIdToFav)
			db.session.add(newFavMovie)
			db.session.commit()


#Add movie to Fav movies from Watched Movie page , on click of Fav button below every movie of Watched Page
@app.route("/_moved_to_Fav")
def moved_to_Fav():
	# Get id of movie from page to add to fav
	newMovieIdToFav = request.args.get('id')

	#Get id of current user
	mail=session['email']
	ed_User = User.query.filter_by(email=mail).first()
	currentuserid = ed_User.uid
	# if Movie is already added to Fav show message it is already added
	if (FavMovies.query.filter_by(user_id=currentuserid,movie_id=newMovieIdToFav).first() is not None) :
			return jsonify(result='movie already added to Fav')
	else :
			#if movie is not in Favorite list add this movie to Favorite movies list		
			newFavMovie = FavMovies(currentuserid , newMovieIdToFav)
			db.session.add(newFavMovie)
			db.session.commit()



#Add movie to Fav movies from Watched Movie page , on click of Fav button below every movie of Watched Page
@app.route("/_moved_to_Watchlist")
def moved_to_Watchlist():
	# Get id of movie from page to add to fav
	newMovieIdToFav = request.args.get('id')

	#Get id of current user
	mail=session['email']
	ed_User = User.query.filter_by(email=mail).first()
	currentuserid = ed_User.uid
	# if Movie is already added to Fav show message it is already added
	if (WatchListMovies.query.filter_by(user_id=currentuserid,movie_id=newMovieIdToFav).first() is not None) :
			return jsonify(result='movie already added to Fav')
	else :
			#if movie is not in Favorite list add this movie to Favorite movies list		
			newFavMovie = WatchListMovies(currentuserid , newMovieIdToFav)
			db.session.add(newFavMovie)
			db.session.commit()
#Discard wrongly added movie from Watched movie list
@app.route('/_remove_from_watched')
def remove_from_watched():
	movieToremove = request.args.get('id')

	mail=session['email']
	ed_User = User.query.filter_by(email=mail).first()
	currentuserid = ed_User.uid

	if (WatchedMovies.query.filter_by(user_id=currentuserid,movie_id=movieToremove).first() is None) :
			return jsonify(result='Movie is already removed')
	else :
			# NEED TO IMPLEMENT Check for Fav if present delete from Fav too
			if (FavMovies.query.filter_by(user_id=currentuserid,movie_id=movieToremove).first() is None) :
				removeMovie = WatchedMovies.query.filter_by(user_id=currentuserid,movie_id=movieToremove).first()
				db.session.delete(removeMovie)
				db.session.commit()

			else : 
				removeMovie = WatchedMovies.query.filter_by(user_id=currentuserid,movie_id=movieToremove).first()
				db.session.delete(removeMovie)
				removeFavMovie = FavMovies.query.filter_by(user_id=currentuserid,movie_id=movieToremove).first()
				db.session.delete(removeFavMovie)
				db.session.commit()
				return jsonify(result=removeMovie.watchedmovies_id)


#Discard wrongly added movie from Favorite list 
@app.route('/_remove_from_fav')
def remove_from_fav():
	movieToremove = request.args.get('id')

	mail=session['email']
	ed_User = User.query.filter_by(email=mail).first()
	currentuserid = ed_User.uid

	if (FavMovies.query.filter_by(user_id=currentuserid,movie_id=movieToremove).first() is None) :
			return jsonify(result='Movie is already removed')
	else :
			#if present in watched and fav delete from Favorite and watched too
			removeMovie = FavMovies.query.filter_by(user_id=currentuserid,movie_id=movieToremove).first()
			db.session.delete(removeMovie)
			db.session.commit()
			return jsonify(result=removeMovie.favmovies_id)


@app.route('/_remove_from_watchList')
def remove_from_watchList() :
	movieToremove = request.args.get('id')
	
	mail=session['email']
	ed_User = User.query.filter_by(email=mail).first()
	currentuserid = ed_User.uid

	if (WatchListMovies.query.filter_by(user_id=currentuserid,movie_id=movieToremove).first() is None) :
			return jsonify(result='Movie is already removed')
	else :
			removeMovie = WatchListMovies.query.filter_by(user_id=currentuserid,movie_id=movieToremove).first()
			db.session.delete(removeMovie)
			db.session.commit()
			return jsonify(result=removeMovie.watchlistmovies_id)



# Go to Watched Page
@app.route("/watched")
def watched():
	if 'email' not in session :
		return redirect(url_for('login'))
	
	else:
		# Get current user id
		mail=session['email']
		ed_User = User.query.filter_by(email=mail).first()
		currentuserid = ed_User.uid
		#Get needed coloumn from Watched MOvies table and pass watchedMovies object to watched page
		watchedMovies = WatchedMovies.query.join(MovieInfo, WatchedMovies.movie_id==MovieInfo.id).add_columns(MovieInfo.poster, MovieInfo.title, MovieInfo.year,  MovieInfo.itemtype , MovieInfo.id).filter(WatchedMovies.movie_id==MovieInfo.id).filter(WatchedMovies.user_id == currentuserid)
		return render_template("watched.html" , watchedMovies = watchedMovies)

# GO to Watchlist page
@app.route("/watchlist")
def watchlist():
	if 'email' not in session :
		return redirect(url_for('login'))
	
	else:
		# Get current user id
		mail=session['email']
		ed_User = User.query.filter_by(email=mail).first()
		currentuserid = ed_User.uid
		#Get needed coloumn from WatchList table and pass myWatchListMovies object to watched page
		myWatchListMovies = WatchListMovies.query.join(MovieInfo, WatchListMovies.movie_id==MovieInfo.id).add_columns(MovieInfo.poster, MovieInfo.title, MovieInfo.year , MovieInfo.itemtype , MovieInfo.id).filter(WatchListMovies.movie_id==MovieInfo.id).filter(WatchListMovies.user_id == currentuserid)
		return render_template("watchlist.html" , myWatchListMovies = myWatchListMovies)

# GO to Favorite page
@app.route("/fav")
def fav():
	if 'email' not in session :
		return redirect(url_for('login'))
	
	else:
		# Get current user id
		mail=session['email']
		ed_User = User.query.filter_by(email=mail).first()
		currentuserid = ed_User.uid
		#Get needed coloumn from Favorite table and pass myFavMovies object to Favorite page
		myFavMovies = FavMovies.query.join(MovieInfo, FavMovies.movie_id==MovieInfo.id).add_columns(MovieInfo.poster, MovieInfo.title, MovieInfo.year , MovieInfo.itemtype ,MovieInfo.id).filter(FavMovies.movie_id==MovieInfo.id).filter(FavMovies.user_id == currentuserid)
		return render_template("favlist.html" , myFavMovies = myFavMovies)


# Go to Feeback page
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

# Go to Log in page
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
