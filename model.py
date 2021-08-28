from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.orm import validates
import re
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
    def set_password(self,password):
        if not password or password == '':
            raise AssertionError('No password provided!')
        self.password = generate_password_hash(password)
    def check_password(self,password):
        check_password_hash(self.password,password)
    @validates('email')
    def validate_email(self,key,email):
        if not email or email == '':
            raise AssertionError('No email provided!')
        if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
            raise AssertionError('Not valid email!')
        if User.query.filter(User.email == email).first():
            raise AssertionError('Email already exist!')
        return email
