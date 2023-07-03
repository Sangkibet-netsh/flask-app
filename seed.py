from faker import Faker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
fake = Faker()


# Generate seed data for the User model
def create_seed_data():
    with app.app_context():
        seed_users = []

        for _ in range(50):
            name = fake.name()
            email = fake.email()
            password = fake.password()

            # Create a new User instance
            user = User(
                name=name,
                email=email,
                password=password
            )
            # Generate a password hash using bcrypt
            user.password_hash = user._generate_password_hash(password).encode('utf-8')
            
            seed_users.append(user)

        # Add seed users to the database
        db.session.bulk_save_objects(seed_users)
        db.session.commit()

        print("Seed data created successfully!")

if __name__ == '__main__':
    create_seed_data()
