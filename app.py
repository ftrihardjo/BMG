from flask import Flask,jsonify,request
from model import db,User
import random, string
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bmg:bmg@192.168.99.101:5432/bmg'
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
if __name__ == '__main__':
    app.run()
