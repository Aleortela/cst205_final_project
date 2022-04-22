from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-wishlist'
bootstrap = Bootstrap5(app)

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

@app.route('/view_wishlist')
def view_list():
   return render_template('view_wishlist.html')
