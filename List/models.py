from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    username = db.Column(db.String(100), nullable =False)
    password = db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class List(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(200),nullable = False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)