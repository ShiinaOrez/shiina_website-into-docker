from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required
from . import auth
from .. import db
#from ..email import email_send
from ..models import User,Text,Arti
from .forms import LoginForm,RegisterForm,PostForm,CPForm,PersonalForm,WAForm

@auth.route('/')
def index():
	return render_template('auth/index.html')

@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        usr=User.query.filter_by(username=form.username.data).first()
        if usr is None:
        	flash('The user is not registed!')
        	return redirect(url_for('login'))
        else:
        	if usr.verify_password(form.password.data):
        		return redirect(url_for('auth.profile',username=form.username.data))
        	else:
        		flash('username or password is wrong!')
        		return redirect(url_for('auth.login'))
    return render_template("auth/login.html",form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('auth.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
	form=RegisterForm()
    	if form.validate_on_submit():
        	usr=User.query.filter_by(username=form.username.data).first()
        	if usr is None:
            		usr=User(username=form.username.data,
                		password=form.password.data,
                		useremail=form.useremail.data)
           		db.session.add(usr)
         		db.session.commit()
#			token=user.generate_confirmation_token()
#			send_email(user.email,'')
            		return render_template("auth/register_create_s.html",name=form.username.data)
        	else:
            		return render_template("auth/register_create_f.html") 
    	return render_template("auth/register.html",form=form)

@auth.route('/profile/',methods=['GET','POST'])
def profile():
#	form=ProfileForm
	usrname=request.args.get('username')
	usr=User.query.filter_by(username=usrname).first()
	return render_template("auth/profile.html",name=usr.username,usr=usr)

@auth.route('/profile_configuration/',methods=['GET','POST'])
def account_configuration():
	usrname=request.args.get('username')
	usr=User.query.filter_by(username=usrname).first()
	return render_template("auth/account_configuration.html",name=usr.username,id=usr.id)

@auth.route('/change_password/',methods=['GET','POST'])
def change_password():
	form=CPForm()
	usrname=request.args.get('username')
	usr=User.query.filter_by(username=usrname).first()
	if form.validate_on_submit():
		usr.password=form.new_password.data
		db.session.add(usr)
		db.session.commit()
		flash('Saved your alteration successful!')
		return redirect(url_for('auth.account_configuration',username=usr.username))
	return render_template("auth/change_password.html",form=form)

@auth.route('/write_articles/',methods=['GET','POST'])
def write_articles():
	form=WAForm()
	usrname=request.args.get('username')
	usr=User.query.filter_by(username=usrname).first()
	if form.validate_on_submit():
		arti=Arti(topic=form.topic.data,txt=form.txt.data,user_id=usr.id)
		db.session.add(arti)
		db.session.commit()
		return redirect(url_for('auth.profile',username=usrname,usr=usr))
	return render_template("auth/profile.html",name=usrname,form=form,usr=usr,write_arti_is_on=1)

@auth.route('/manage_articles/',methods=['GET','POST'])
def manage_articles():
	usrname=request.args.get('username')
	usr=User.query.filter_by(username=usrname).first()
	return render_template("auth/manage_articles.html",usr=usr)

@auth.route('/delete_articles/',methods=['GET','POST'])
def delete_articles():
	usrname=request.args.get('username')
#	usr=User.query.filter_by(username=usrname).first()
	id=request.args.get('arti_id')
	arti=Arti.query.filter_by(id=id).first()
	db.session.delete(arti)
	db.session.commit()
	usr=User.query.filter_by(username=usrname).first()
	return redirect(url_for('auth.manage_articles',username=usrname,usr=usr))

@auth.route('/post_text/',methods=['GET','POST'])
def post_text():
	form=PostForm()
	usrname=request.args.get('username')
	usr=User.query.filter_by(username=usrname).first()
	if form.validate_on_submit():
		txt=Text(incl=form.incl.data,user_id=usr.id)
		db.session.add(txt)
		db.session.commit()
		return redirect(url_for('auth.activities',username=usr.username))
	return render_template("auth/post_text.html",form=form)
		
@auth.route('/activities/',methods=['GET','POST'])
def activities():
	usrname=request.args.get('username')
	texts=Text.query.all()
	return render_template("auth/activities.html",texts=texts,username=usrname)

@auth.route('/change_personal_s/',methods=['GET','POST'])
def change_personal_s():
	form=PersonalForm()
	usrname=request.args.get('username')
	usr=User.query.filter_by(username=usrname).first()
	if form.validate_on_submit():
		usr.personal_s=form.signal.data
		db.session.add(usr)
		db.session.commit()
		return redirect(url_for('auth.profile',username=usr.username))
	return render_template("auth/change_personal_s.html",form=form)
