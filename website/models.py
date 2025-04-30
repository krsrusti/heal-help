from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    blood_sugar_logs = db.relationship('BloodSugar', back_populates='user')


class BloodSugar(db.Model):
    __tablename__ = 'blood_sugar_log'
    
    id = db.Column(db.Integer, primary_key=True)
    meal_time = db.Column(db.String(100))
    log_date = db.Column(db.String(100))
    blood_sugar_level = db.Column(db.Integer)
    sugar_type = db.Column(db.String(50))
    category = db.Column(db.String(50)) 

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='blood_sugar_logs')
