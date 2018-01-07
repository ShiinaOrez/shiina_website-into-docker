import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = 'hard to guess string'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	FLASKY_MAIL_SUBJECT_PREFIX='[Flasky]'
	FLASKY_MAIL_SENDER='Flasky Admin <shiina_orez@qq.com>'
	FLASKY_ADMIN='shiina'

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG=True
	MAIL_SERVER='smtp.qq.com'
	MAIL_POST=465
	MAIL_USE_TLS=True
	MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI =\
    		'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
	TESTING=True
	SQLALCHEMY_DATABASE_URI =\
    		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI =\
    		'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config={
	'developments': DevelopmentConfig,
	'testing': TestingConfig,
	'production':ProductionConfig,
	'default':DevelopmentConfig
}
