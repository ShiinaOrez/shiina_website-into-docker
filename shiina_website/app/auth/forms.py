from flask_wtf import Form
from wtforms import BooleanField,StringField,SubmitField,PasswordField
from wtforms import ValidationError
from wtforms.validators import Length,Email,EqualTo
from ..models import User

class ManageForm(Form):
	arti_topic=BooleanField('Topic:')
	submit=SubmitField('Delete')

class WAForm(Form):
	topic=StringField('Topic:',validators=[Length(1,20)])
	txt=StringField('Main Text:',validators=[Length(1,2000)])
	submit=SubmitField('Submit')

class PersonalForm(Form):
	signal=StringField('Your Signal:',validators=[Length(0,300)])
	submit=SubmitField('Submit')

class CPForm(Form):
	pre_password=StringField('Old password:',validators=[Length(3,20)])
	new_password=PasswordField('New password:',validators=[Length(3,20),EqualTo('new_password2',message='Passwords do not match')])
	new_password2=StringField('Password again:',validators=[Length(3,20)])
	submit=SubmitField('Submit')

class LoginForm(Form):
	username=StringField('Username:',validators=[Length(3,20)])
 	password=PasswordField('Password:',validators=[Length(3,20)])
	remeber_me=BooleanField('Keep me login in')
 	submit=SubmitField('Login')

class PostForm(Form):
#	topic=StringField('Topic:')
#	date=StringField('Date:')
	incl=StringField('MainText:',validators=[Length(3,1000)])
	submit=SubmitField('POST')

class RegisterForm(Form):
	username=StringField('Username:',validators=[Length(3,20)])
 	password=PasswordField('Password:',validators=[Length(3,20),EqualTo('password2',message='Passwords do not match')])
	password2=StringField('Password again:',validators=[Length(3,20)])
	useremail=StringField('Your email:',validators=[Email()])
	submit=SubmitField('Register now')
