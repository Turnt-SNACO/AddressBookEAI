# Author: James Anderson
# EAI Coding Challenge: Address Book

from flask import Flask, render_template, request, session
from elasticsearch import Elasticsearch
from ElasticAB import ElasticAB

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def home_page():
    host = request.args.get("host")
    port = request.args.get("port")
    if (host is not None and port is not None):
        session['host'] = host
        session['port'] = port
        print(session['host'], session['port'])
        return render_template('indexc.html')
    #display index page
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    #display add form
    name = request.args.get("name")
    address = request.args.get("addr")
    phone_number = request.args.get("phnm")
    if (name is not None and address is not None and phone_number is not None):
        eab = ElasticAB(session['host'], session['port'])
        print(session['host'], session['port'])
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
        eab = ElasticAB(session['host'], session['port'])
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
        eab = ElasticAB(session['host'], session['port'])
        result = eab.search_contact(name)
        if result is False:
            return "NO"
        return render_template('search_res.html', name_r=result.name, addr_r=result.address, phnm_r=result.phone_number)
    #display search form
    return render_template('search.html')

@app.route('/delete')
def delete_contact():
    name = request.args.get("name")
    if name is not None:
        eab = ElasticAB(session['host'], session['port'])
        result = eab.delete_contact(name)
        if result is False:
            return "Error occured"
        return render_template('deletec.html')
    #display delete form
    return render_template('delete.html')
if __name__ == '__main__':
    app.run()