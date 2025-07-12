from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    location = db.Column(db.String(120))
    profile_photo = db.Column(db.String(256))
    availability = db.Column(db.String(120))
    public = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    skills = db.relationship('Skill', secondary=user_skills, back_populates='users')
    swap_requests_sent = db.relationship('SwapRequest', foreign_keys='SwapRequest.requestor_id', back_populates='requestor')
    swap_requests_received = db.relationship('SwapRequest', foreign_keys='SwapRequest.receiver_id', back_populates='receiver')

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', secondary=user_skills, back_populates='skills')

class SwapRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requestor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    accepted = db.Column(db.Boolean, default=False)
    requestor = db.relationship('User', foreign_keys=[requestor_id], back_populates='swap_requests_sent')
    receiver = db.relationship('User', foreign_keys=[receiver_id], back_populates='swap_requests_received') 