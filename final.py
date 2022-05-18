# Course: CST 205
# Title: Drinkr
# Abstract: a cocktail webapp(Drinkr) where the user can create an account, login, and add different types of cocktails to their wishlist.
# Authors: Onyinye Aladiume, Alec Ortega, ?
# Date: 5/18/2022
# Who worked on what- 
 # Home.html: Onyi
 # LoginPage.htm: Alec
 # Products.html: Onyi
 # ProfilePage.html: Alec
 # Signup: Onyi
 # view_drinklist.html: Alec

from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_bootstrap import Bootstrap5
from flask_nav import Nav
from flask_nav.elements import Navbar, View
import re
import sqlite3 as sql
from api_test import Products as product

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'csumb-wishlist'
app.secret_key = 'csumb-wishlist'
app.config["DEBUG"] = True
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
bootstrap = Bootstrap5(app)
nav = Nav()

def store_item(drinkName,username):
   conn = get_db_connect()
   cursor = conn.cursor()
   drink_name = drinkName
   user = username
   params = [drink_name, user]
   cursor.execute('INSERT INTO drinksnew VALUES (NULL,?,?)', params)
   conn.commit()
   
def get_db_connect():
   try:
      conn = sql.connect('database.db')
      conn.row_factory = sql.Row
   except sql.error as e:
      print(e)
   return conn
    
@nav.navigation()
def homenavbar():
   return Navbar('Drinkr', View('ACCOUNT LOGIN','login'),
                 View('SIGN UP', 'signup'), View('PRODUCTS', 'products'))
nav.init_app(app)

@nav.navigation()
def profilenavbar():
    return Navbar('Drinkr', View('PRODUCTS', 'products'), View('LOGOUT', 'logout'))
nav.init_app(app)

@nav.navigation()
def productsnavbar():
    return Navbar('Drinkr', View('HOME', 'home'), View('ACCOUNT','profile'), View('LOGOUT', 'logout'))
nav.init_app(app)

@nav.navigation()
def listnavbar():
   return Navbar('Drinkr', View('ACCOUNT LOGIN','login'), View('PRODUCTS', 'products'))
nav.init_app(app)

@nav.navigation()
def loginnavbar():
    return Navbar('Drinkr', View('HOME', 'home'))
nav.init_app(app)
 
       
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

#This function/route shows how a user signs up. User sessions is being used so, if a username and password
#is found in the database, a message will appear. But if a username & password isn't in the database it will insert those 
#two values into the db accordingly.
#Source referenced: https://www.geeksforgeeks.org/login-and-registration-project-using-flask-and-mysql/?ref=gcse
@app.route('/signup', methods=['GET', 'POST'])
def signup():
   msg = ''
   conn = get_db_connect()
   cursor = conn.cursor()
   session.permanent = True
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
         session['username'] = username
         session['password'] = password
         user= {'username': session['username'],
                'password': session['password']}
         msg = 'You have successfully registered !'
         return render_template('profile_page.html', msg=msg, user=user)
   elif request.method == 'POST':
      msg = 'Please fill out the form !'

   return render_template('signup.html', msg = msg)

# products() shows that if a user is logged in and gets to the products' route, data is fetched from the api to display 
# product names images, and instructions. 
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

# The view list functions takes in an id as a parameter when initialized. It then goes on to do an API query with the ID
# through our API file apit_test.py which is imported as "product".  With this it call the lookupdrinks function and with the
# drink id that has been inherited it pulls the correct drink which it stores into data_1. From there some fancy indexing helps us obtain
# the data from the data_1 object.
# Sources accessed: https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
@app.route("/view_drinklist/<id>", methods=['GET','POST'])
def view_list(id):
    if 'username' in session: 
        if request.method == 'GET':
            drinkid = id
            drinks = []
            data_1= product.lookupdrinks(drinkid)
            conn =  get_db_connect()
            cursor = conn.cursor()
            if data_1 is not None:
                id1 = data_1['drinks'][0]['idDrink']
                drinkName = data_1['drinks'][0]['strDrink']
                product_image1 = data_1['drinks'][0]['strDrinkThumb']
                store_item(drinkName, session['username'])
                params = [session['username']]
                cursor.execute('SELECT drink_name FROM drinksnew WHERE user = ?', params)
                for row in cursor.fetchall():
                    for i in range(0, len(cursor.fetchall())):
                        drinks[i] = row
                    return render_template('view_drinklist.html',id1=id1, productName1 = drinkName, 
                                       v2=product_image1, drinks = drinks)
            else:
                return "data_1 is empty"

# The login pages starts by assigning its conn and cursor variables for our db query.
# It then takes the information entered and stores them in username and password variables.
# With those variables created we then store them in  the session created by session.permanent.
# If the db query fins a user matching the username and password then we redirect to the profile.
# Sources accessed: https://flask-login.readthedocs.io/en/latest/
# https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/
# https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
@app.route('/LoginPage', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        conn = get_db_connect()
        cursor = conn.cursor()
        session.permanent = True
        username = request.form['usrnm']
        password = request.form['pwd']
        session['username'] = username
        session['password'] = password
        params = [username, password]
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', params)
        user = [cursor.fetchone()]
        if password != "":
            if user is not None:
                flash(f'{username} login Successful', 'info')
                return redirect(url_for('profile'))
    else:
        if 'user' in session:
            return redirect(url_for('profile'))
        return render_template('LoginPage.html')

# Simple logout route that does not render anything. It only terminates the session and redirects
# to the login page afterwards.
# Sources accessed https://pythonbasics.org/flask-sessions/
@app.route('/logout', methods = ['GET','POST'])
def logout():
    if 'username' in session:
        user = session['username']
        flash(f'{user} logout Successful', 'info')
    session.pop('username', None)
    return redirect(url_for('login'))

# This route was initially working but for some reason the userid I was passing off through the
# different routes decided to stop working the day before the demo.
# Sources accessed: https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
@app.route('/edit', methods=['GET', 'POST'])
def useredit():
    if 'username' in session:
        if request.method == 'POST':
            conn = get_db_connect()
            cursor = conn.cursor()            
            username = request.form['usrnm']
            password = request.form['pwd']
            session['username'] = username
            session['password'] = password
            params = [username, password]
            cursor.execute('UPDATE users SET username = ?, password = ?'
                                   'WHERE user = ?', params)
            flash(f'{username} was successfully updated','info')
            conn.commit()
            return redirect(url_for('profile'))

# The profile route checks to see if we have the necessary variables stored in our session object.
# Once the check is completed we create a user dictionary to populate the input fields and pass it
# through render_template. 
@app.route('/profile_page', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        if 'password' in session:
            user= {'username': session['username'],
                   'password': session['password']}
            if user is not None:
                return render_template('profile_page.html',user=user)
        else:
            return redirect(url_for('profile'))
    else:
        return render_template('LoginPage.html')


