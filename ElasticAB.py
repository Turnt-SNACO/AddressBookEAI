# Author: James Anderson
# This class interacts with the Elasticsearch data store of contacts
# The datastore will index by name since name must be a unique field
# Supported fields are name, address, and phone number

from elasticsearch import Elasticsearch
from Contact import Contact
INDEX='contacts'

class ElasticAB:
    #Will have default of localhost and port 9200 if unspecified
    def __init__(self, address='localhost', port='9200'):
        self.address = address
        self.port = port
        self.es = Elasticsearch([{'host': address, 'port' : port}])

    #Add a contact if it does not already exist otherwise
    #Returns boolean value which indicates success or failure
    def add_contact(self, name, address, phone_number):
        name = name.lower()
        if not self.has(name):
            body = {"name":name,"address":address,"phnm":phone_number}
            self.es.create(index=INDEX, doc_type='_doc', id=name, body=body)
            return True
        return False
    
    #Get contact information if it exists
    #Returns a contact object
    def search_contact(self, name):
        name = name.lower()
        if self.has(name):
            data = self.es.get(index=INDEX, doc_type='_doc', id=name)['_source']
            contact = Contact(data['name'], data['address'], data['phnm'])
            return contact
        return False
    
    #Update existing contact
    #Returns boolean value which indicates success or failure
    def update_contact(self, name, address, phone_number):
        if self.has(name):
            body = {"name":name,"address":address,"phnm":phone_number}
            self.es.update(index=INDEX, doc_type='_doc', id=name, body=body)
            return True
        return False

    #Delete an existing contact
    #Returns boolean value which indicates success or failure
    def delete_contact(self, name):
        name = name.lower()
        if self.has(name):
            self.es.delete(index=INDEX, doc_type='_doc', id=name)
            return True
        return False

    #List a subset of results in alphabetical order
    #   epp - entries per page
    #   page - starts at 0
    #returns a list of contact objects with results of search
    def list_contacts(self, epp, page):
        frm = epp*(page)
        body = {"query": {"match_all" : {}}}
        data = self.es.search(index=INDEX, doc_type='_doc', from_=frm, size=epp, body=body)
        entries = []
        for i in data['hits']['hits']:
            entry = Contact(i['_source']['name'], i['_source']['address'], i['_source']['phnm'])
            entries.append(entry)
        return entries

    #Shorthand to make typing easier
    def has(self, name):
        return self.es.exists(index=INDEX, doc_type='_doc', id=name)


