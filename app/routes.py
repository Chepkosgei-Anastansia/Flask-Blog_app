from app import app,db
from flask import render_template

from app.forms import EditProfileForm, LoginForm, RegistrationForm # import LoginForm class from forms.py 
from flask.helpers import flash, url_for
from flask import redirect
from app.models import User
from flask_login import login_required,logout_user,login_user,current_user
from flask import request
from werkzeug.urls import url_parse
from _datetime import datetime



@app.route('/')
@app.route('/index')   ##associates the URLs to this function

# flasks invokes the function and pass the return value back to the browser as a response
#
@login_required
def index():
    user={'username':'Anastansia'}
    posts = [
        {
            'author': {'username': 'Angela'},
            'body':'Beautiful day in PortLand'
        },
        {
           'author':{'username': 'Agatha'},
           'body':'The Avengers movie was cool'
        }
    ]


    return render_template('index.html', title='Home', posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():
    # used to prevent logged in user from navigating into the login page
    # redirects to the index page
    # is_authenticated method checks whether the user is logged in or not
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm() #instantiates LogInForm class from forms.py and send it to template
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()  # first()--executes a query, when you only need to have one result
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or password')
            return redirect(url_for('login'))

        login_user(user,remember=form.remember_me.data)
        #If the user navigates to /index, for example, the @login_required decorator will intercept the request and respond with a redirect to /login, but it will add a query string argument to this URL, making the complete redirect URL /login?next=/index. The next query string argument is set to the original URL, so the application can use that to redirect back after login.
        #Here is a snippet of code that shows how to read and process the next query string argument:
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for(next_page))
        

    return render_template('login.html',title='Sign In', form= form)


     # logout 
@app.route('/logout')
def logout():
            #Flask-Login's logout_user()
    logout_user()
    return redirect(url_for('index'))


#User Registration
@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')

        return redirect(url_for('login'))

    return render_template('register.html',title='Register', form=form)

# user profile method
#view function only accessible to logged in users
#has dynamic component ('/user/<username>')
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404() # loads user from db
    posts = [
        {'author':user,'body':'Test post #1'},
        {'author':user,'body':'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)
# 
#the decorator registers the decorated function to be executed right before the view function
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

#
@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',title='Edit Profile',form='form')


