# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # Database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/database_name'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize SQLAlchemy
# db = SQLAlchemy(app)

# @app.route('/')
# def about():
#     return 'index.html'


# # Define User model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     # Add any other fields as required

# # Define UploadedImage model
# class UploadedImage(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(100), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     user = db.relationship('User', backref=db.backref('images', lazy=True))
#     # Add any other fields as required

# if __name__ == '__main__':
#     # Create tables if they do not exist
#     db.create_all()
#     app.run(debug=True)

#////////////////////////////////////////////////////////////////////////////////////////
# from flask import Flask,render_template
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# # app = Flask(__name__, static_url_path='/custom_static')
# # app.static_folder = 'static'

# # Database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:rithu2005@localhost/'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize SQLAlchemy
# db = SQLAlchemy(app)

# @app.route('/')
# def about():
#     return render_template("index.html")

# @app.route('/multImage')
# def mult_image():
#     return render_template('multImag.html')

# @app.route('/video')
# def video():
#     return render_template('video.html')


# # Define User model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     # Add any other fields as required

# # Define UploadedImage model
# class UploadedImage(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(100), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     user = db.relationship('User', backref=db.backref('images', lazy=True))
#     # Add any other fields as required

# if __name__ == '__main__':
#     # Create tables if they do not exist within application context
#     with app.app_context():
#         db.create_all()
    
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:rithu2005@localhost/video_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT configuration
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'
jwt = JWTManager(app)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Define UploadedImage model
class UploadedImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('images', lazy=True))

# Route for user registration
@app.route('/register', methods=['GET','POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    hashed_password = generate_password_hash(password)

    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

# Route for user login
@app.route('/login', methods=['GET','POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid username or password"}), 401

# Protected route
@app.route('/home', methods=['GET','POST'])
@jwt_required()
def home():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/')
def about():
    return render_template("index.html")

@app.route('/multImage')
def mult_image():
    return render_template('multImag.html')

@app.route('/video')
def video():
    return render_template('video.html')



if __name__ == '__main__':
    # Create tables if they do not exist within application context
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)

