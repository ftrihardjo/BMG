from flask import Flask,jsonify,request
from model import db,User
import random, string
import jwt
import hashlib
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bmg:bmg@192.168.99.101:5432/bmg'
app.config['SECRET_KEY'] = 'Drmhze6EPcv0fN_81Bj-nA'
db.init_app(app)
db.create_all(app=app)
@app.route('/register',methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        name = data['name']
        email = data['email']
        referral_code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        user = User(username=username,password=password,name=name,email=email,referral_code=referral_code)
        db.session.add(user)
        db.session.commit()
        return jsonify({'status':'ok'})
    except AssertionError as error:
        return jsonify({'status':'{0}'.format(error)})
@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter(User.username == username).one()
    token = jwt.encode({'username':username,'password':password},app.config['SECRET_KEY'],algorithm='HS256')
    return jsonify({'name':user.name,'email':user.email,'referral_code':user.referral_code,'token':token})
@app.route('/edit',methods=['POST'])
def edit():
    try:
        data = request.get_json()
        token = data['token']
        user = User.query.filter(User.username == data['username']).one()
        if not token or token == '':
            raise AssertionError('No token provided!')
        payload = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
        if user.username != payload['username'] or user.password != hashlib.md5(payload['password'].encode()).hexdigest():
            raise AssertionError('Invalid token!')
        user.password = data['password']
        user.name = data['name']
        user.email = data['email']
        db.session.commit()
        return jsonify({'status':'ok'})
    except AssertionError as error:
        return jsonify({'status':'{0}'.format(error)})
@app.route('/ref_code',methods=['POST'])
def ref_code():
    try:
        data = request.get_json()
        token = data['token']
        if not token or token == '':
            raise AssertionError('No token provided!')
        payload = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
        user = User.query.filter(User.username == payload['username']).one()
        if data['referral_code'] == user.referral_code:
            return jsonify({'status':'ok'})
        return jsonify({'status':'invalid'})
    except AssertionError as error:
        return jsonify({'status':'{0}'.format(error)})
if __name__ == '__main__':
    app.run()
