# Author: James Anderson
# EAI Coding Challenge: Address Book

from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port' : '9200'}])

@app.route('/', methods=['GET', 'POST'])
def home_page():
    #display index page
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    #display add form
    return render_template('add.html')

@app.route('/update', methods=['GET', 'POST'])
def update_contact():
    #display update form
    return render_template('update.html')


@app.route('/list')
def get_contact_list():
    #display list form
    return render_template('list.html')

@app.route('/search')
def get_contact(name):
    #display search form
    return render_template('search.html')

@app.route('/delete')
def delete_contact():
    #display delete form
    return render_template('delete.html')