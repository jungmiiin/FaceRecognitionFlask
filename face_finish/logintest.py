from flask import Flask, Blueprint, render_template, flash,  Response, request, redirect,url_for
from flask_login import login_required, current_user
from __init__ import create_app, db
app = create_app()
main = Blueprint('main', __name__)

@app.route("/")
def home():
    return render_template('index2.html')

@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@app.route("/home")
def mainpage():
    return render_template('home.html')

if __name__=='__main__':
    app.run(debug=True)    