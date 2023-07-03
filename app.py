from flask import Flask, jsonify, request,json
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)



class UserResource(Resource):
    def get(self):
        users = User.query.all()
        user_list = []
        for user in users:
            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            user_list.append(user_data)
        return jsonify(user_list)

    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        if not name or not email or not password:
            return jsonify({'error': 'Missing required fields'}), 400

        user = User(name, email, password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201


class UserDetailResource(Resource):
    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        name = data.get('name')
        email = data.get('email')

        if name:
            user.name = name
        if email:
            user.email = email

        db.session.commit()
        return jsonify({'message': 'User updated successfully'})

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})

class PasswordResource(Resource):
    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        password = data.get('password')
        if not password:
            return jsonify({'error': 'Missing required field: password'}), 400

        user.password_hash = user._generate_password_hash(password).decode('utf-8')
        db.session.commit()
        return jsonify({'message': 'Password updated successfully'})


api.add_resource(UserResource, '/users')
api.add_resource(UserDetailResource, '/users/<int:user_id>')
api.add_resource(PasswordResource, '/users/<int:user_id>/password')



if __name__ == '__main__':
    app.run(port=5555)