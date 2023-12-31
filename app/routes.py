from flask import render_template, redirect, request, url_for, session, flash
import bcrypt
from app import app, db
from app import sentiment_analyzer as sa
from app.models import Users

# Route for the main page or login page
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This route handles the login page, where users can log in with their email and password.

    - Checks if the user's credentials are valid.
    - If the user is authenticated, it stores their email in the session.
    - Redirects to the home page upon successful login.
    - Displays an error message if the login fails.

    Methods:
        - GET: Displays the login form.
        - POST: Processes the login form submission.

    Returns:
        - GET: Login form.
        - POST: Home page or error message.
    """
    msg = ''
    if request.method == "POST" and 'password' in request.form and 'email' in request.form:
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                session['email'] = user.email
                session['username'] = user.username
                return redirect(url_for('home'))
            else:
                msg = 'Password did not match. Please enter the correct password.'
        else:
            msg = 'User does not exist. Please create an account.'

    return render_template('login.html', msg=msg)

# Route for registration/sign-up page
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    This route handles the registration/sign-up page.

    - Allows users to create a new account with a username, email, and password.
    - Validates the email and checks if the email already exists in the database.
    - Hashes the password before storing it in the database.
    - Stores the user's email in the session upon successful registration.
    - Flashes a success message upon successful registration.

    Methods:
        - GET: Displays the registration form.
        - POST: Processes the registration form submission.

    Returns:
        - GET: Registration form.
        - POST: Home page or error message.
    """
    msg = ''
    if request.method == "POST" and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()

        if user:
            msg = 'User already exists. Please try to log in.'
        else:
            hashed_password =  bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = Users(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            session['username'] = username
            flash('Registration successful!', 'success')
            return redirect(url_for('home'))

    return render_template('register.html', msg=msg)

# Route for the home page
@app.route('/home', methods=["GET", "POST"])
def home():
    """
    This route handles the home page, which is accessible after a user logs in.

    - Checks if the user is logged in by verifying the presence of their email in the session.
    - Redirects to the login page if the user is not logged in.
    - Displays the home page if the user is authenticated.

    Returns:
        - Home page if the user is logged in.
        - Login page if the user is not logged in.
    """
    email = session.get('email')
    if email:
        if request.method == "POST" and 'keyword' in request.form and 'comments' in request.form:
            keyword = request.form['keyword']
            comments = request.form['comments']

            rsa = sa.RedditSentimentAnalysis()
            overall_sentiment, confidence_level, keyword_freq, pie_chart_path, word_cloud_path = rsa.download_data(keyword, comments)
            pie_chart = pie_chart_path.replace("app/static", "", 1)
            word_cloud = word_cloud_path.replace("app/static", "", 1)

            return render_template('results.html', overall_sentiment=overall_sentiment, confidence_level=confidence_level,
                                    keyword_freq=keyword_freq, pie_chart=pie_chart, word_cloud=word_cloud)
        return render_template('home.html')
    return render_template('login.html')  # Redirect to the login page if the user is not logged in

# Route for user logout
@app.route('/logout')
def logout():
    """
    This route handles user logout.

    - Removes the 'email' key from the session to log the user out.
    - Redirects to the login page after logout.

    Returns:
        - Login page after logout.
    """
    session.pop('email', None)  # Remove the 'email' key from the session to log out the user
    session.pop('username', None) # Remove the 'username' key from the session to log out the user
    return redirect(url_for('login'))  # Redirect to the login page after logout
