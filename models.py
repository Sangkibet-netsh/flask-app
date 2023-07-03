import hashlib
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = self._generate_password_hash(password)

    def _generate_password_hash(self, password):
        hash_algo = hashlib.sha256()
        hash_algo.update(password.encode('utf-8'))
        return hash_algo.hexdigest()

    def verify_password(self, password):
        hashed_password = self._generate_password_hash(password)
        return self.password_hash == hashed_password