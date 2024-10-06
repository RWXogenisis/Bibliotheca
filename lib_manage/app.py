from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from passlib.context import CryptContext
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/library_management'
app.secret_key = 'your_secret_key'  # Use a strong and unique secret key in production
mongo = PyMongo(app)

# Password hashing context for scrypt
pwd_context = CryptContext(schemes=["scrypt"], default="scrypt")

def get_smtp_credentials():
    credentials = mongo.db.SMTP_Credentials.find_one({"_id": "smtp_credentials"})
    if credentials:
        return credentials['smtp_user'], credentials['smtp_password']
    else:
        raise Exception("SMTP credentials not found in the database")

def send_email(to_email, otp):
    # Debugging prints
    print(f"Recipient Email: {to_email}")

    # Email configuration
    EMAIL_USE_SSL = True
    EMAIL_HOST = 'smtp.zoho.in'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = 'genisistesting@zohomail.in'  # Your Zoho email
    EMAIL_HOST_PASSWORD = 'gentesting@123'  # Your Zoho password
    DEFAULT_FROM_EMAIL = 'genisistesting@zohomail.in'  # Your Zoho email
    SERVER_EMAIL = 'genisistesting@zohomail.in'  # Your Zoho email

    # Email details
    subject = 'Your OTP Code'
    body = f'Your OTP code is {otp}'
    # from_email = EMAIL_HOST_USER  # Using the Zoho email

    # Create the message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = DEFAULT_FROM_EMAIL
    msg['To'] = to_email

    # Send the email
    try:
        server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)  # Using SSL
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)  # Login to the server
        server.sendmail(DEFAULT_FROM_EMAIL, [to_email], msg.as_string())  # Send email
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')
    finally:
        server.quit()  # Ensure the server is closed properly


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        user = mongo.db.Users.find_one({'username': username})

        if user:
            otp = random.randint(100000, 999999)
            session['otp'] = otp
            session['username'] = username

            send_email(user['Email'], otp)
            return redirect(url_for('verify_otp'))
        else:
            flash('Username does not exist. Please try again.')
            return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html')


@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp = request.form.get('otp')  # Use .get() to avoid KeyError
        if otp and int(otp) == session.get('otp'):
            return redirect(url_for('reset_password'))
        else:
            flash('Invalid OTP')
    return render_template('verify_otp.html')


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            hashed_password = pwd_context.hash(new_password)
            mongo.db.Users.update_one({'username': session.get('username')}, {'$set': {'password': hashed_password}})
            session.pop('otp', None)
            session.pop('username', None)
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match')
    return render_template('reset_password.html')

@app.route('/dashboard')
def dashboard():
    current_username = session.get('username')  # Get the username from the session
    if not current_username:
        return redirect(url_for('login'))  # Redirect if not logged in

    # Fetch user data from MongoDB using the current username
    user = mongo.db.Users.find_one({'username': current_username})
    membership = user["MembershipType"]

    return render_template('dashboard.html', user=user, member=membership)

@app.route('/downloads')
def downloads():
    current_username = session.get('username')  # Get the username from the session
    if not current_username:
        return redirect(url_for('login'))  # Redirect if not logged in

    # Fetch user data from MongoDB using the current username
    user = mongo.db.Users.find_one({'username': current_username})
    membership = user["MembershipType"]

    return render_template('downloads.html', user=user, member=membership)

@app.route('/myLibrary')
def myLibrary():
    current_username = session.get('username')
    if not current_username:
        return redirect(url_for('login'))

    user = mongo.db.Users.find_one({'username': current_username})
    user_id = str(user["_id"])  # Convert ObjectId to string

    membership = user["MembershipType"]

    # Fetch fines, issued books, requests, and reservations using the user_id
    fines = list(mongo.db.Fines.find({'UserID': user_id}))
    issued_books = list(mongo.db.Issues.find({'UserID': user['_id']}))
    requested_books = list(mongo.db.Requests.find({'UserID': user['_id']}))
    reservations = list(mongo.db.Reservations.find({'UserID': user['_id']}))
    print(reservations, sep="\n")

    return render_template('myLibrary.html', user=user, member=membership, fines=fines, issued_books=issued_books, requests=requested_books, reservations=reservations)

@app.route('/make_request', methods=['POST'])
def make_request():
    book_id = request.form.get('bookID')
    current_username = session.get('username')
    
    if not current_username or not book_id:
        return redirect(url_for('myLibrary'))

    user = mongo.db.Users.find_one({'username': current_username})
    
    # Check if a request exists
    existing_request = mongo.db.Requests.find_one({
        'UserID': user['_id'],
        'BookID': book_id
    })
    
    if not existing_request:
        new_request = {
            'UserID': user['_id'],
            'BookID': book_id,
            'RequestDate': str(datetime.now().date()),
            'Status': 'Requested'
        }
        mongo.db.Requests.insert_one(new_request)

    return redirect(url_for('myLibrary'))

@app.route('/make_reservation', methods=['POST'])
def make_reservation():
    book_id = request.form.get('bookID')
    current_username = session.get('username')
    
    if not current_username or not book_id:
        return redirect(url_for('myLibrary'))

    user = mongo.db.Users.find_one({'username': current_username})
    
    # Check if a reservation already exists
    existing_reservation = mongo.db.Reservations.find_one({
        'UserID': user['_id'],
        'BookID': book_id
    })
    
    if not existing_reservation:
        new_reservation = {
            'UserID': str(user['_id']),  # Convert ObjectId to string for consistency
            'BookID': book_id,
            'ReservationDate': str(datetime.now().date()),  # Current date as ReservationDate
            'Status': "Pending"  # Set status to "Pending"
        }
        mongo.db.Reservations.insert_one(new_reservation)

    return redirect(url_for('myLibrary'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.Users.find_one({'username': username})

        if user and pwd_context.verify(password, user['password']):
            session['username'] = username  # Store the username in session
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    flash('You have been logged out successfully.')  # Optional: Flash message
    return redirect(url_for('login'))  # Redirect to the login page


if __name__ == '__main__':
    app.run(debug=True)
