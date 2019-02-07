# Author: James Anderson
# EAI Coding Challenge: Address Book

from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from ElasticAB import ElasticAB

app = Flask(__name__)
eab = ElasticAB()
@app.route('/', methods=['GET', 'POST'])
def home_page():
    #display index page
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    #display add form
    name = request.args.get("name")
    address = request.args.get("addr")
    phone_number = request.args.get("phnm")
    if (name is not None and address is not None and phone_number is not None):
        success = eab.add_contact(name, address, phone_number)
        if success:
            return render_template('addc.html')
        else:
            return render_template('addf.html')
    return render_template('add.html')

@app.route('/update', methods=['GET', 'POST'])
def update_contact():
    name = request.args.get("name")
    address = request.args.get("addr")
    phone_number = request.args.get("phnm")
    if (name is not None and address is not None and phone_number is not None):
        success = eab.update_contact(name, address, phone_number)
        if success:
            return render_template('updatec.html')
        else:
            return render_template('updatef.html')
    #display update form~
    return render_template('update.html')

@app.route('/list')
def get_contact_list():
    #display list form
    return render_template('list.html')

@app.route('/search')
def get_contact():
    name = request.args.get("name")
    if name is not None:
        result = eab.search_contact(name)
        if result is False:
            return "NO"
        return render_template('search_res.html', name_r=result.name, addr_r=result.address, phnm_r=result.phone_number)
    #display search form
    return render_template('search.html')

@app.route('/delete')
def delete_contact():
    #display delete form
    return render_template('delete.html')