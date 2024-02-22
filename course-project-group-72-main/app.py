from flask import Flask, render_template, redirect,url_for,request, jsonify,session
import mysql.connector
from mysql.connector import Error
from flask_bcrypt import Bcrypt
import jwt
import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key_here'  
# print("hi")
# Replace 'username', 'password', 'hostname', and 'database_name' with your MySQL credentials
mysql_config = {
    'host': 'localhost',
    'database': 'user_auth',
    'user': 'root',
    'password': 'rithu2005'
}

def connect_to_mysql():
    try:
        conn = mysql.connector.connect(**mysql_config)
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(e)

def close_connection(conn):
    if conn.is_connected():
        conn.close()
        print('Connection to MySQL database closed')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    conn = connect_to_mysql()
    cursor = conn.cursor(dictionary=True)

    username = request.form['username']
    email = request.form['email']
    fullname = request.form['fullname']
    password = request.form['password']

    # Check if the username or email already exists
    cursor.execute("SELECT * FROM user_details WHERE username = %s OR email = %s", (username, email))
    existing_user = cursor.fetchone()
    if existing_user:
        close_connection(conn)
        return jsonify({'message': 'Username or email already exists'}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Insert the new user into the database
    insert_query = "INSERT INTO user_details (username, email, name, password) VALUES (%s, %s, %s, %s)"
    user_data = (username, email, fullname, hashed_password)
    cursor.execute(insert_query, user_data)
    conn.commit()

    close_connection(conn)
    # return jsonify({'message': 'User signed up successfully'}), 201
    return redirect(url_for('mult_image'))  # Redirect to the success route



@app.route('/multImage')
def mult_image():
    return render_template('multImag.html')



@app.route('/video')
def video():
    return render_template('video.html')


#  @app.route('/success')
# def success():
#     # Render the success page
#     return render_template('success.html')
#     return jsonify({'message': 'User signed up successfully'}), 201

@app.route('/login', methods=['POST','GET'])
def login():
    conn = connect_to_mysql()
    cursor = conn.cursor(dictionary=True)

    username = request.form['username']
    password = request.form['password']

    # Query the user from the database
    cursor.execute("SELECT * FROM user_details WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user['password'], password):
        # Generate JWT token
        session['username']=username
        token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
        close_connection(conn)
        return redirect(url_for('user_profile'))
        # return redirect(url_for('mult_image')) 
    #     return jsonify({'token': token.decode('utf-8')}), 200                                                                                                               
    else:
         error_message = 'Invalid username or password'
         return render_template('index.html', error_message=error_message)
        # close_connection(conn)
        # return jsonify({'message': 'Invalid username or password'}), 401
        

# if __name__ == '__main__':
#     app.run(debug=True)


# import mysql.connector
# from flask import Flask, render_template, session, redirect, url_for

# app = Flask(__name__)
# app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

# # Function to connect to MySQL database
def connectt_to_mysql():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='rithu2005',
        database='user_auth'
    )

@app.route('/user_profile',methods=['POST','GET'])
def user_profile():
    # session['username']=username
    # Check if user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login page if user is not logged in

    # Retrieve logged-in user's details from database
    conn = connectt_to_mysql()
    cursor = conn.cursor(dictionary=True)
    username = session['username']
    cursor.execute("SELECT * FROM user_details WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()

    # Render user profile template with user's details
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
