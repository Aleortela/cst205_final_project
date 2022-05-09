from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo
import re
import sqlite3 as sql
from datetime import datetime
import sys
import json
from api_test import Products

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-wishlist'
app.config["DEBUG"] = True
bootstrap = Bootstrap5(app)
product = Products()

# mysql = MySQL(app)
def get_db_connect():
   try:
      conn = sql.connect('database.db')
      conn.row_factory = sql.Row
   except sql.error as e:
      print(e)
   return conn

class Wishlist(FlaskForm):
   list_item = StringField('Wishlist Item', validators=[DataRequired()])

wishlist = []

def store_item(my_item):
   wishlist.append(dict(
      item  = my_item,
      date = datetime.today()))


@app.route('/', methods=('GET', 'POST'))
def home():
   form = Wishlist()
   if form.validate_on_submit():
      store_item(form.list_item.data)
      return redirect('/view_playlist')

   
   return render_template('home.html', form = form)

@app.route('/signup', methods=('GET', 'POST'))
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
         username = request.form['username']
         password = request.form['password']
         params = (username, password)
         cursor.execute('INSERT INTO users VALUES (NULL,?,?)', params)
         conn.commit()
         msg = 'You have successfully registered !'
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

@app.route('/view_wishlist')
def view_list():
   return render_template('view_wishlist.html')