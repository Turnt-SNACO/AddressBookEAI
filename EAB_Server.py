# Author: James Anderson
# EAI Coding Challenge: Address Book

from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from elasticsearch import NotFoundError
from ElasticAB import ElasticAB
import sys

app = Flask(__name__)

#get host and port data from config
f = open('eab.config', 'r')
lines = f.readlines()
host = lines[0].replace('\n', '')
port = lines[1]

# Gets a list of contacts that match the passed query
# if no query is passed it will default to all but
# will still only display the desired ammount and 
# page offset
@app.route('/contact', methods=['GET'])
def search_contacts():
    pageSize = request.args.get('pageSize')
    page = request.args.get('page')
    query = request.args.get('query')
    eab = ElasticAB(host=host, port=port)
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
        return "An unexpected error occured\n"
    

# creates a new contact with the given information
# requires name, address, phone number and email
# however they may be empty strings if that data
# does not need to be added to the contact
@app.route('/contact', methods=['POST'])
def create_contact():
    data = request.get_json(force=True)
    eab = ElasticAB(host=host, port=port)
    if eab.has(data['name'].lower()):
        return 'Contact already exists, try updating instead.\n'
    try:
        if (len(data['name'] > 100)):
            return 'Name cannot be over 100 characters long.\n'
        if (len(data['address'] > 150)):
            return 'Address cannot be over 150 characters long.\n'
        if (len(data['phnm']) > 15):
            return 'Phone number cannot be over 15 characters long.\n'
        if (len(data['email']) > 40):
            return 'Email cannot be over 40 characters long.\n'
        eab.add_contact(data['name'], data['address'], data['phnm'], data['email'])
    except KeyError:
        return 'Missing data. Make sure to include name, address, phone number, and email even if they are empty strings.\n'
    return "Contact created\n"

# finds the contact by the given name
@app.route('/contact/<name>', methods=['GET'])
def get_contact(name):
    if len(name) > 100:
        return 'Name cannot be over 100 characters long.\n'
    eab = ElasticAB(host=host, port=port)
    try:
        result = eab.search_contact(name)
    except NotFoundError:
        return 'Contact by that name could not be found [404].\n'
    except ValueError as e:
        return str(e)
    return beautify(result.name, result.address, result.email_address, result.phone_number)

# upadtes the contents of a specified contact
@app.route('/contact/<name>', methods=['PUT'])
def update_contact(name):
    data = request.get_json(force=True)
    try:
        eab = ElasticAB(host=host, port=port)
        try:
            if (len(data['name'] > 100)):
                return 'Name cannot be over 100 characters long.\n'
            if (len(data['address'] > 150)):
                return 'Address cannot be over 150 characters long.\n'
            if (len(data['phnm']) > 15):
                return 'Phone number cannot be over 15 characters long.\n'
            if (len(data['email']) > 40):
                return 'Email cannot be over 40 characters long.\n'
            eab.update_contact(data['name'], data['address'], data['phnm'], data['email'])
        except KeyError:
            return 'Missing data. Make sure to include name, address, phone number, and email even if they are empty strings.\n'
        except Exception as e:
            return str(e)
        return 'Contact updated successfully.\n'
    except NotFoundError:
        return 'Contact not found [404].  Try creating a contact instead.\n'

# deletes the contact specified by name
@app.route('/contact<name>', methods=['DELETE'])
def delete_contact(name):
    try:
        if (len(data['name'] > 100)):
            return 'Name cannot be over 100 characters long.\n'
        eab = ElasticAB(host=host, port=port)
        eab.delete_contact(name)
        return 'Contact deleted successfully.\n'
    except NotFoundError:
        return 'Cannot delete, contact not found [404].\n'

# used to format a contact nicely
def beautify(name, address, email_address, phone_number):
    return '{0}\n\t{1}\n\t{2}\n\t{3}\n\n'.format(name, address.replace('\n', '\n\t'), email_address, phone_number)

if __name__ == '__main__':
    app.run()