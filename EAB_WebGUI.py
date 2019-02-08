# Author: James Anderson
# EAI Coding Challenge: Address Book

from flask import Flask, render_template, request, session
from elasticsearch import Elasticsearch
import elasticsearch
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
    name = request.args.get("name")
    address = request.args.get("addr")
    phone_number = request.args.get("phnm")
    email_address = request.args.get("email")
    #this will trigger if none of the form has been filled previously
    if (name is None and address is None and phone_number is None and email_address is None):
        return render_template('add.html')
    #check for one non-name field
    has_one_field = (address != "" or phone_number != "" or email_address != "")
    if (name is not None and has_one_field):
        #initialize an EAB with specified host and port, this will cause an error if not specified per session.
        eab = ElasticAB(session['host'], session['port'])
        success = eab.add_contact(name, address, phone_number, email_address)
        if success:
            return render_template('addc.html')
        else:
            #this shouldn't get hit ever but is there just in case
            return render_template('addf.html')
    else:
        # loads this page if only name field is filled 
        # to prompt for at least one more data field
        return render_template('addmore.html', name=name)
    

@app.route('/update', methods=['GET', 'POST'])
def update_contact():
    name = request.args.get("name")
    address = request.args.get("addr")
    phone_number = request.args.get("phnm")
    email_address = request.args.get("email")
    if (name is None and address is None and phone_number is None and email_address is None):
        #first load
        return render_template('update.html')
    has_one_field = (address != "" or phone_number != "" or email_address != "")
    if (name is not None and has_one_field):
        eab = ElasticAB(session['host'], session['port'])
        success = eab.update_contact(name, address, phone_number)
        if success:
            return render_template('updatec.html')
    else:
        return render_template('updatemore.html', name=name)

@app.route('/list')
def get_contact_list():
    epp = request.args.get("epp")
    p = request.args.get("p")
    if epp is not None and p is not None:
        eab = ElasticAB(session['host'], session['port'])
        entries = eab.list_contacts(int(epp), int(p))
        return list_parser(entries)
    #display list form
    return render_template('list.html')

@app.route('/search')
def get_contact():
    name = request.args.get("name")
    if name is not None:
        eab = ElasticAB(session['host'], session['port'])
        try:
            result = eab.search_contact(name)
            return render_template('search_res.html', name_r=result.name, addr_r=result.address, phnm_r=result.phone_number, email_r=result.email_address)
        except elasticsearch.NotFoundError:
            return render_template('notfound.html')
    #display search form
    return render_template('search.html')

@app.route('/delete')
def delete_contact():
    name = request.args.get("name")
    if name is not None:
        eab = ElasticAB(session['host'], session['port'])
        result = eab.delete_contact(name)
        if result is True:
            return render_template('deletec.html')
        else:
            return result
        
    #display delete form
    return render_template('delete.html')

#transforms list of contacts into a pretty html list
def list_parser(entries):
    data = '<!DOCTYPE html><html><title>EAB for EAI</title><meta name="list" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css"><body><header class="w3-container w3-teal"><h1>Elastic Address Book</h1></header>'
    for i in entries:
        data = data + '<div class="w3-container w3-half w3-margin-top"><div class="w3-container w3-card-4" method="GET">' + i.name +":<br> " + i.address +"<br> " + i.email_address + "<br>" + i.phone_number +"<br>" + '</div></div>'
    data = data + '</body></html>'
    return data

if __name__ == '__main__':
    app.run(debug=True)

