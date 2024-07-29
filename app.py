from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://carpool_user:password@localhost/carpool_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from auth import auth_bp
from group import group_bp
from ride import ride_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(group_bp, url_prefix='/api')
app.register_blueprint(ride_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
