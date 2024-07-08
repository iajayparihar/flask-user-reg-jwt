from flask import Flask
from auth import auth_bp
from datetime import timedelta
app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/auth')

# Configure the PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key01'  
app.config['SECRET_KEY'] = 'your_secret_key01'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


@app.route('/')
def home():
    return 'Home page'


from controller import *

if __name__ == '__main__':
    app.run(debug=True)