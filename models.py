from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    secret = db.Column(db.String(120), unique=True, nullable=False)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    method_id = db.Column(db.Integer, nullable=False)
    data_in = db.Column(db.Text, nullable=False)
    params = db.Column(db.JSON, nullable=False)
    data_out = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    time_out = db.Column(db.Float, nullable=False)
    user = db.relationship('User', backref=db.backref('sessions', lazy=True))
