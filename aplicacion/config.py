import os

SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'#os.random(16)

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/bdcampeonato'
SQLALCHEMY_TRACK_MODIFICATIONS = False