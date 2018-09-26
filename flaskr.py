from pymongo import MongoClient

from flask import render_template
from flask import Flask

client = MongoClient()
db = client.feedbackdb

app = Flask(__name__)
@app.route('/')
def index():
        return 'Index Page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
@app.route('/show_entries')
def show_entries():
    #cur = g.db.execute('select title, text from entries order by id desc')
    #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    cursor = db.feedbackdb.find({"from_user.username" : "r0mk_h0ze" } )
    entries =  cursor 
    return render_template('show_entries.html', entries=entries)
