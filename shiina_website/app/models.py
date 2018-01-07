from . import db,login_manager
from flask import current_app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin,current_user

class User(UserMixin,db.Model):
 	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(20),unique=True)
    	password=db.Column(db.String(20))
        password_hash=db.Column(db.String(128))
	useremail=db.Column(db.String(30),unique=True)
	personal_s=db.Column(db.String(600))
	texts=db.relationship('Text',backref='user')
	artis=db.relationship('Arti',backref='user')
	role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
        @property
        def password(self):
            raise AttributeError('password is not a readable attribute')
	@password.setter
        def password(self,password):
            self.password_hash=generate_password_hash(password)
        def verify_password(self,password):
            return check_password_hash(self.password_hash,password)
	def __init__(self,**kwargs):
		super(User,self).__init__(**kwargs)
#		if self.role is None:
#			if self.useremail==current_app.config['FLASK_ADMIN']:
#				self.role=Role.query.filter_by(permissions=0xff).first()
#			if self.role_id is None:
#				self.role_id=Role.query.filter_by(default=True).first()
	def can(self,permissions):
		return self.role_id is not None and (self.role_id.permissions&permissions)==permissions
	def is_administrator(self):
		return self.can(Permission.ADMINISTER)
	def generate_auth_token(self,expiration):
		s=Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
		return s.dumps({'id':self.id})
	@staticmethod
	def verify_auth_token(token):
		s=Serializer(current_app.config['SECRET_KEY'])
		try:
			data=s.loads(token)
		except:
			return None
		return User.query.get(data['id'])
class Text(db.Model):
	__tablename__='texts'
	id=db.Column(db.Integer,primary_key=True)
#	topic=db.Column(db.String(20))
#	date=db.Column(db.String(20))
	incl=db.Column(db.String(1000))
	user_id=db.Column(db.Integer,db.ForeignKey('users.id'))

class Arti(db.Model):
	__tablename__='artis'
	id=db.Column(db.Integer,primary_key=True)
	topic=db.Column(db.String(20))
	txt=db.Column(db.String(2000))
	user_id=db.Column(db.Integer,db.ForeignKey('users.id'))

class Role(db.Model):
	__tablename__='roles'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(64),unique=True)
	default=db.Column(db.Boolean,default=False,index=True)
	permissions=db.Column(db.Integer)
	users=db.relationship('User',backref='role',lazy='dynamic')
	@staticmethod
	def insert_roles():
		roles={
			'User':(Permission.FOLLOW|
				Permission.COMMENTS|
				Permission.WRITE_ARTICLES,True),
			'Moderator':(Permission.FOLLOW|
					Permission.COMMENTS|
					Permission.WRITE_ARTICLES|
					Permission.MODERATE_COMMENTS,False),
			'Administrator':(0xff,False)
		}	
		for r in roles:
			role=Role.query.filter_by(name=r).first()
			if role is None:
				role=Role(name=r)
			role.permissions=roles[r][0]
			role.default=roles[r][1]
			db.session.add(role)
		db.session.commit()


class Permission:
	FOLLOW=0x01
	COMMENT=0x02
	WRITE_ARTICLES=0x04
	MODERATE_COMMENTS=0x08
	ADMINISTER=0x80

class AnonymousUser(AnonymousUserMixin):
	def can(self,permissions):
		return false
	def is_administrator(self):
		return false

login_manager.anonymous_user=AnonymousUser

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
