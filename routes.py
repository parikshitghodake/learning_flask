from flask import Flask, render_template, request , session , redirect , url_for , flash , jsonify
from models import db , User , Feedback , Movie , MovieInfo
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


@app.route('/_add_numbers')
def add_numbers():
    Title = request.args.get('Title')
    year = request.args.get('releaseYear')
    ImdbID = request.args.get('imdbID')
    Plot = request.args.get('Plot')
    Poster = request.args.get('Poster')
    newMovie = MovieInfo(ImdbID , Title , year , Plot , Poster)
    db.session.add(newMovie)
    db.session.commit()
    return jsonify(result=Title+year)
    


@app.route("/watched")
def watched():
	watchedMovies = MovieInfo.query.all()#db.execute('SELECT title , poster from movieinfo_t')
	return render_template("watched.html" , watchedMovies = watchedMovies)



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
