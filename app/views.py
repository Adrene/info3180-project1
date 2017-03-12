"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app
from app import db
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from forms import LoginForm
from models import UserProfile
from time import strftime #generates time user is added
from datetime import date, datetime
import random # generates userID
from flask import session
from flask import jsonify
from werkzeug import secure_filename
from models import UserProfile




UPLOAD_FOLDER = '.app/static/uploads'
app.config ['UPLOAD FOLDER']=UPLOAD_FOLDER


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

def getTime():
    return time.strftime("%a, %d %b %Y")
    

@app.route('/profile/')
def profile():
    form = LoginForm()
    if request.method == "GET" and form.validate_on_submit():
        userid  = random.randint(1, 1000)
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        age = form.age.data
        gender = form.gender.data
        bio = form.bio.data
        pwd = form.pwd.data
        file = request.files['img']
        img = secure_filename(file.filename)
        date_added = datetime.now().strftime("%a, %d, %b, %Y")  
        file.save(os.path.join("app/static/uploads", img))
        
        new_user= UserProfile(userid, first_name, last_name, username, age. gender, bio, pwd, img, date_added)
        db.session.add(new_user)
        db.session.commit()
        
        flash ("Sign up successful")
        return redirect(url_for('home'))
            
    return render_template('profile.html', form=form)




@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            
            flash('You were logged in')
            return redirect(url_for('allprofile'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
