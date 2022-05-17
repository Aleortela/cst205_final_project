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
import sys, json, jsonify
from api_test import Products as product


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'csumb-wishlist'
app.secret_key = 'csumb-wishlist'
app.config["DEBUG"] = True
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
bootstrap = Bootstrap5(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
nav = Nav()

class Drink(FlaskForm):
   drink_name = StringField('Enter a drink', validators=[DataRequired()])
   
   
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

product = Products()


def get_db_connect():
   try:
      conn = sql.connect('database.db')
      conn.row_factory = sql.Row
   except sql.error as e:
      print(e)
   return conn

def store_item(my_item,userid):
   conn = get_db_connect()
   cursor = conn.cursor()
   drink_name = my_item
   userid = userid
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
        store_item(form.drink_name.data, session['username'])
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
      msg = 'Please fill out the form!'
   return render_template('signup.html', msg = msg, username=username)

@app.route('/products')
def products():
    if 'username' in session:
        data_5 = product.get_random_products()
        #data_6 = product.search_cocktail()
        id = data_5['drinks'][0]['idDrink']
        id2 = data_5['drinks'][1]['idDrink']
        productName_1 = data_5['drinks'][0]['strDrink']
        productName_2 = data_5['drinks'][1]['strDrink']
        product_image = data_5['drinks'][0]['strDrinkThumb']
        product_image2 = data_5['drinks'][1]['strDrinkThumb']
        product_description_1 = data_5['drinks'][0]['strInstructions']
        product_description_2 = data_5['drinks'][1]['strInstructions']
        return render_template('products.html', productName1 = productName_1, productName2 = productName_2, 
                          productDes = product_description_1, productDes2= product_description_2, 
                          image1=product_image, image2 = product_image2, id = id, id2=id2)
    else:
        return redirect(url_for('login'))

@app.route('/view_drinklist/<id>', methods=['GET','POST'])
def view_list(id):
    if 'username' in session: 
        if request.method == 'GET':
            drinkid = id
            data_1= product.lookupdrinks(drinkid)
            conn =  get_db_connect()
            cursor = conn.cursor()
            if data_1 is not None:
                id1 = data_1['drinks'][0]['idDrink']
                productName_11 = data_1['drinks'][0]['strDrink']
                product_image1 = data_1['drinks'][0]['strDrinkThumb']
                cursor = cursor.execute('SELECT drink_name FROM drinks')
                return render_template('view_drinklist.html',id1=id1, productName1 = productName_11, 
                                       v2=product_image1)
            else:
                return "data_1 is empty"

@app.route('/LoginPage', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        conn = get_db_connect()
        cursor = conn.cursor()
        session.permanent = True
        username = request.form['usrnm']
        session['username'] = username
        password = request.form['pwd']
        params = [username, password]
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', params)
        user = [cursor.fetchone()]
        session['userid'] = user[0][0]
        if user is not None:
            flash(f'{username} login Successful', 'info')
            return redirect(url_for('profile'))
    else:
        if 'user' in session:
            return redirect(url_for('profile'))
        return render_template('LoginPage.html')
    
@app.route('/logout', methods = ['GET','POST'])
def logout():
    if 'username' in session:
        user = session['username']
        flash(f'{user} logout Successful', 'info')
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/edit', methods=['GET', 'POST'])
def useredit():
    if 'userid' in session:
        if request.method == 'POST':
            conn = get_db_connect()
            cursor = conn.cursor()            
            username = request.form['usrnm']
            session['username'] = username
            password = request.form['pwd']
            params = [username, password, session['userid']]
            cursor.execute('UPDATE users SET username = ?, password = ?'
                                   'WHERE userid = ?', params)
            flash(f'{username} was successfully updated','info')
            conn.commit()
            return redirect(url_for('profile'))
            
            
    

@app.route('/profile_page', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        user= {'username': session['username'],
               'password': session['password']}
        if user is not None:
            return render_template('profile_page.html',user=user)
    else:
        return render_template('LoginPage.html')
    
