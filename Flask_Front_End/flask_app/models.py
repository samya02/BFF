from sqlalchemy.orm import backref
from flask_app import db, login_manager,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db. ForeignKey('user.id'), nullable= False)
    img = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"Order('{self.user_id}','{self.img}')"
    

class Legal_Advisor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer,db.ForeignKey('user.id'), nullable= False)
    name = db.Column(db.String(20), nullable=False)
    profile = db.Column(db.String(100), unique=True)
    year = db.Column(db.Integer, nullable= False)
    role = db.Column(db.String(15), nullable=False)
    city = db.Column(db.String(15), nullable=False)
    country = db.Column(db.String(15), nullable=False)
    awards = db.Column(db.Integer, nullable= False)
    cases = db.Column(db.Integer, nullable= False)
    advised = db.Column(db.Integer, nullable= False)
    union = db.Column(db.Integer, nullable= False)
    description = db.Column(db.String(150), nullable=False)
    request = db.Column(db.Boolean , default= False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    pic = db.Column(db.String(120), nullable=False, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png')

    def __repr__(self):
        return f"Order('{self.user}','{self.profile}','{self.name}','{self.phone}','{self.email}','{self.pic}')"