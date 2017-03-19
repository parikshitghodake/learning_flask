from flask_wtf import Form
from wtforms import StringField , PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired , Email , Length

class SignupForm(Form) :
	first_name = StringField('First Name' , validators=[DataRequired('Please Enter your First Name')])
	last_name = StringField('Last Name', validators=[DataRequired('Please Enter your Last Name')])
	email = StringField('Email', validators=[DataRequired('Please Enter your Email address') , Email('Please Enter Valid Email Address')])
	password = PasswordField('Password', validators=[DataRequired('Please Enter your Password') , Length(min=6 , message='Password Should be min of 6 characters')])
	submit = SubmitField('Sign Up')

class LoginForm(Form):
	email = StringField('Email', validators=[DataRequired('Please Enter your Email Address') , Email('Please Enter Valid Email Address')])
	password = PasswordField('Password' , validators=[DataRequired('Please Enter your Password') , Length(min=6 , message='Password Should be min of 6 characters')])
	submit = SubmitField('Sign In')

class FeedbackForm(Form):
	first_name = StringField('First Name' , validators=[DataRequired('Please Enter your Name')])
	email = StringField('Email', validators=[DataRequired('Please Enter Your Email Address') , Email('Please Enter Valid Email')])
	comments = StringField('Comments' , validators=[DataRequired('Please enter your comments')])
	submit = SubmitField('Submit')

class SearchMovie(Form):
	movie_name = StringField('Movie Name' , validators=[DataRequired('Enter Movie Name')])
	year = HiddenField('Year')
	submit = SubmitField('Search')
	watched = SubmitField('Watched')
	watchlist = SubmitField('Watchlist')
	fav = SubmitField('Favorite')
