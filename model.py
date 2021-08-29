from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re
import hashlib
db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    username = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    name = db.Column(db.String,nullable=False)
    email = db.Column(db.String,unique=True,nullable=False)
    referral_code = db.Column(db.String)
    @validates('username')
    def validate_username(self,key,username):
        if not username or username == '':
            raise AssertionError('No username provided!')
        if User.query.filter(User.username == username).first():
            raise AssertionError('Username already exist!')
        return username
    @validates('password')
    def validate_password(self,key,password):
        if not password or password == '':
            raise AssertionError('No password provided!')
        return hashlib.md5(password.encode()).hexdigest()
    @validates('email')
    def validate_email(self,key,email):
        if not email or email == '':
            raise AssertionError('No email provided!')
        if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
            raise AssertionError('Not valid email!')
        if User.query.filter(User.email == email).first():
            raise AssertionError('Email already exist!')
        return email
    @validates('name')
    def validate_name(self,key,name):
        if not name or name == '':
            raise AssertionError('No name provided!')
        return name
