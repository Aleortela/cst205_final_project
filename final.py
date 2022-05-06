from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
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

# mysql = MySQL(app)
def get_db_connect():
   try:
      conn = sql.connect('database.db')
      conn.row_factory = sql.Row
   except sql.error as e:
      print(e)
   return conn

class Drink(FlaskForm):
   drink_name = StringField('Enter a drink', validators=[DataRequired()])


def store_item(my_item):
   conn = get_db_connect()
   cursor = conn.cursor()
   drink_name = my_item
   userid = 00
   params = [drink_name, userid]
   cursor.execute('INSERT INTO drinks VALUES (NULL,?,?)', params)
   conn.commit()


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
         username = request.form['username']
         password = request.form['password']
         params = (username, password)
         cursor.execute('INSERT INTO users VALUES (NULL,?,?)', params)
         conn.commit()
         msg = 'You have successfully registered !'
   elif request.method == 'POST':
      msg = 'Please fill out the form !'

   return render_template('signup.html', msg = msg)
   #return render_template('signup.html', error=error)

@app.route('/view_drinklist', methods=['GET'])
def view_list():
   conn =  get_db_connect()
   cursor = conn.cursor()
   
   if request.method == 'GET':
       cursor = conn.execute('SELECT * FROM drinks')
       for row in cursor.fetchall():
           drinks = {'id': row[0], 
                     'drink_name': row[1],
                     'userid': row[2]}
           if drinks is not None:
               return jsonify(drinks)
       
   conn.commit()
   return render_template('view_drinklist.html', drinks=drinks)

