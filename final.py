from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flask_login import (LoginManager, UserMixin, login_required,
login_user, logout_user, current_user)
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo
import re
import sqlite3 as sql
from datetime import datetime
import sys, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-wishlist'
app.config["DEBUG"] = True
bootstrap = Bootstrap5(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
nav = Nav()

class Drink(FlaskForm):
   drink_name = StringField('Enter a drink', validators=[DataRequired()])
   
class Login(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    #remember = BooleanField('Remember Me')
    submit = SubmitField('login')
   
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.authenticated = False
    
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return self.authenticated()
    def is_active(self):
        return True
    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connect()
    cursor = conn.cursor()
    params = [user_id]
    cursor.execute('SELECT * FROM users WHERE username = (?)', params)
    user = cursor.fetchone()
    if user is None:
        return 'Not a valid user'
    else:
        return User(int(user[0]),user[1],user[2])

def get_db_connect():
   try:
      conn = sql.connect('database.db')
      conn.row_factory = sql.Row
   except sql.error as e:
      print(e)
   return conn

def store_item(my_item):
   conn = get_db_connect()
   cursor = conn.cursor()
   drink_name = my_item
   userid = 00
   params = [drink_name, userid]
   cursor.execute('INSERT INTO drinks VALUES (NULL,?,?)', params)
   conn.commit()


@nav.navigation()
def mynavbar():
   return Navbar('Drinkr', View('ACCOUNT LOGIN','login'),View('SIGN UP', 'signup'))
nav.init_app(app)
        
@app.route('/', methods=['GET', 'POST'])
def home():
   form = Drink()
   if form.validate_on_submit():
      store_item(form.drink_name.data)
      msg = 'Successfully added!'
      return render_template('view_drinklist.html', msg = msg)

   return render_template('home.html', form = form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
   msg = ''
   conn = get_db_connect()
   cursor = conn.cursor()
   if request.method == "POST" and 'username' in request.form and 'password' in request.form:
      username = request.form['username']
      password = request.form['password']
      cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password, ))
      account = cursor.fetchone()
      if account:
         msg = 'Account already exists !'
      elif not re.match(r'[A-Za-z0-9]+', username):
         msg = 'Username must contain only characters and numbers !'
      elif not username or not password:
         msg = 'Please fill out the form !'
      else:
         params = (username, password)
         cursor.execute('INSERT INTO users VALUES (NULL,?,?)', params)
         conn.commit()
         msg = 'You have successfully registered !'
         return render_template('profile_page.html', msg=msg)
   elif request.method == 'POST':
      msg = 'Please fill out the form !'

   return render_template('signup.html', msg = msg, username=username)
   #return render_template('signup.html', error=error)

@app.route('/view_drinklist', methods=['GET','POST'])
def view_list():
    drinks = []
    conn =  get_db_connect()
    cursor = conn.cursor()
    cursor.execute('SELECT drink_name FROM drinks')
    if request.method == 'GET':
        for row in cursor.fetchall():
            for i in range(0, len(cursor.fetchall())):
               drinks[i] = row
               if drinks is not None:
                  return drinks
               else:
                   return "Drinks is empty!"
              
    conn.commit()
    return render_template('view_drinklist.html',len = len(drinks),drinks=drinks)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if form.validate_on_submit():
        conn = get_db_connect()
        cursor = conn.cursor()
        username = request.form['username']
        password = request.form['password']
        params = [username, password]
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', params)
        user = [cursor.fetchone()]
        Us = load_user(user[0])
        if form.username.data == Us.username and form.password.data == Us.password:
           login_manager.login_user(Us, remember=form.remember.data)
           msg = 'Successful Login'
           return render_template('profile_page.html', user=Us)
    return render_template('LoginPage.html',form=form)

@app.route('/profile_page', methods=['GET', 'POST'])
def profile():
   conn = get_db_connect()
   cursor = conn.cursor()
   
   return render_template('profile_page.html')
