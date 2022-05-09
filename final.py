from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from flask_login import LoginManager
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo
import re
import sqlite3 as sql
from datetime import datetime
import sys
import json,jsonify
from api_test import Products


app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-wishlist'
app.config["DEBUG"] = True
bootstrap = Bootstrap5(app)
login_manager = LoginManager()
nav = Nav()

class Drink(FlaskForm):
   drink_name = StringField('Enter a drink', validators=[DataRequired()])

product = Products()


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

def read_db():
    conn = get_db_connect()
    cursor = conn.cursor()
    table = []
    cursor = conn.execute('SELECT * FROM drinks')
    for row in cursor.fetchall():
        for i in range(0, len((cursor.fetchall()))):
            table[i] = row

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
      
   return render_template('signup.html', msg = msg)

@app.route('/products')
def products():
   data_5 = product.get_random_products()
   data_6 = product.search_cocktail()
   productName_1 = data_5['drinks'][0]['strDrink']
   productName_2 = data_5['drinks'][0]['strDrink']
   
   product_image = data_5['drinks'][0]['strDrinkThumb']

   product_description_1 = data_6['ingredients'][0]['strIngredient']
   return render_template('products.html', productName1 = productName_1, productName2 = productName_2, productDes = product_description_1, image1=product_image)

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
    conn = get_db_connect()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            params = [username, password]
            conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', params)
            user = cursor.fetchall()
            if user:
                render_template('profile_page.html',username=username)
            
    return render_template('LoginPage.html')

@app.route('/profile_page', methods=['GET', 'POST'])
def profile():
   conn = get_db_connect()
   cursor = conn.cursor()
   
   return render_template('profile_page.html')
