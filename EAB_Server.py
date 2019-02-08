# Author: James Anderson
# EAI Coding Challenge: Address Book

from flask import Flask, render_template, request, session
from elasticsearch import Elasticsearch
import elasticsearch
from ElasticAB import ElasticAB
import sys

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Gets a list of contacts that match the passed query
# if no query is passed it will default to all but
# will still only display the desired ammount and 
# page offset
@app.route('/contact', methods=['GET'])
def search_contacts():
    pageSize = request.args.get('pageSize')
    page = request.args.get('page')
    query = request.args.get('query')
    eab = ElasticAB()
    try:
        if query is None:
            results = eab.search_by_query(pageSize, page)
        else:
            results = eab.search_by_query(pageSize, page, query)
        if results == []:
            return 'Search came back empty.'
        else:
            output = ''
            for i in results:
                output += beautify(i.name, i.address, i.email_address, i.phone_number)
            return output
    except Exception:
        return "an error occured\n"

# creates a new contact with the given information
# requires name, address, phone number and email
# however they may be empty strings if that data
# does not need to be added to the contact
@app.route('/contact', methods=['POST'])
def create_contact():
    data = request.get_json(force=True)
    eab = ElasticAB()
    if eab.has(data['name'].lower()):
        return 'Contact already exists, try updating instead.\n'
    try:
        eab.add_contact(data['name'], data['address'], data['phnm'], data['email'])
    except KeyError:
        return 'Missing data. Make sure to include name, address, phone number, and email even if they are empty strings.\n'
    return "Contact created\n"

# finds the contact by the given name
@app.route('/contact/<name>', methods=['GET'])
def get_contact(name):
    eab = ElasticAB()
    try:
        result = eab.search_contact(name)
    except elasticsearch.NotFoundError:
        return 'Contact by that name could not be found.\n'
    return beautify(result.name, result.address, result.email_address, result.phone_number)

# upadtes the contents of a specified contact
@app.route('/contact/<name>', methods=['PUT'])
def update_contact(name):
    data = request.get_json(force=True)
    try:
        eab = ElasticAB()
        try:
            eab.update_contact(data['name'], data['address'], data['phnm'], data['email'])
        except KeyError:
            return 'Missing data. Make sure to include name, address, phone number, and email even if they are empty strings.\n'
        return 'Contact updated successfully.\n'
    except elasticsearch.NotFoundError:
        return 'Contact not found.  Try creating a contact instead.\n'

# deletes the contact specified by name
@app.route('/contact<name>', methods=['DELETE'])
def delete_contact(name):
    try:
        eab = ElasticAB()
        eab.delete_contact(name)
        return 'Contact deleted successfully.\n'
    except elasticsearch.NotFoundError:
        return 'Contact not found, cannot delete.\n'

# used to format a contact nicely
def beautify(name, address, email_address, phone_number):
    return '{0}\n\t{1}\n\t{2}\n\t{3}\n\n'.format(name, address.replace('\n', '\n\t'), email_address, phone_number)

if __name__ == '__main__':
    app.run(debug=True)