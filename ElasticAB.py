# Author: James Anderson
# This class interacts with the Elasticsearch data store of contacts
# The datastore will index by name since name must be a unique field
# Supported fields are name, address, email address and phone number

from elasticsearch import Elasticsearch
import elasticsearch
from Contact import Contact
import sys
INDEX='contacts'

class ElasticAB:
    #Will have default of localhost and port 9200 if unspecified
    #If the index for contacts does not exist it will make one
    def __init__(self, host='localhost', port='9200'):
        self.host = host
        self.port = port
        self.es = Elasticsearch([{'host': host, 'port' : port}])
        if not self.es.indices.exists(INDEX):
            body = {"settings" : {"number_of_shards":1, "number_of_replicas":0}}
            self.es.indices.create(index=INDEX, body=body)

    #Add a contact if it does not already exist otherwise
    #Returns boolean value which indicates success or failure
    def add_contact(self, name, address='', phone_number='', email_address=''):
        if (not isinstance(name, str) or not isinstance(address, str) or not isinstance(phone_number, str)):
            raise TypeError("Arguments must be strings")
        if len(name) > 100:
            raise Exception("Name field must be less than 100 characters")
        if len(address) > 150:
            raise Exception("Address field must be less than 150 characters")
        if len(email_address) > 100:
            raise Exception("Email address must be less than 100 characters")
        #according to a quick google search, the longest existing phone numbers are 15 digits long
        if len(phone_number) > 15:
            raise Exception("Phone number must be less than 16 characters")
        id_ = name.lower()
        if not self.has(id_):
            body = {"name":name,"address":address,"phnm":phone_number,"email":email_address}
            self.es.create(index=INDEX, doc_type='_doc', id=id_, body=body)
            return True
        return False
    
    #Get contact information if it exists
    #Returns a contact object
    def search_contact(self, name):
        if (not isinstance(name, str)):
            raise TypeError("Argument must be string")
        if len(name) > 100:
            raise Exception("Name field must be less than 100 characters")
        id_ = name.lower()
        if self.has(id_):
            data = self.es.get(index=INDEX, doc_type='_doc', id=id_)['_source']
            contact = Contact(name=data['name'].capitalize(), address=data['address'], phone_number=data['phnm'], email_address=data['email'])
            return contact
        raise elasticsearch.NotFoundError("The contact by that name does not exist in the data store")
    
    #Update existing contact
    #Returns boolean value which indicates success otherwise raises error
    def update_contact(self, name, address='', phone_number='', email_address=''):
        if (not isinstance(name, str) or not isinstance(address, str) or not isinstance(phone_number, str)):
            raise TypeError("Arguments must be strings")
        if len(name) > 100:
            raise Exception("Name field must be less than 100 characters")
        if len(address) > 150:
            raise Exception("Address field must be less than 150 characters")
        if len(email_address) > 100:
            raise Exception("Email address must be less than 100 characters")
        #according to a quick google search, the longest existing phone numbers are 15 digits long
        if len(phone_number) > 15:
            raise Exception("Phone number must be less than 16 characters")
        id_ = name.lower()
        if self.has(id_):
            if address == '':
                address = self.search_contact(name).address
            if phone_number == '':
                phone_number = self.search_contact(name).phone_number
            if email_address == '':
                email_address = self.search_contact(name).email_address
            body = {"script" : {"source" : "ctx._source.address = params.address; ctx._source.phnm = params.phnm; ctx._source.email = params.email","lang" : "painless","params": {"address" : address,"phnm" : phone_number, "email":email_address}}}
            self.es.update(index=INDEX, doc_type='_doc', id=id_, body=body)
            return True
        raise elasticsearch.NotFoundError("Can't update a contact that doesn't exist! Try using add instaed.")

    #Delete an existing contact
    #Returns boolean value which indicates success otherwise raises error
    def delete_contact(self, name):
        if (not isinstance(name, str)):
            raise TypeError("Arguments must be strings")
        if len(name) > 100:
            raise Exception("Name field must be less than 100 characters")
        name = name.lower()
        if self.has(name):
            self.es.delete(index=INDEX, doc_type='_doc', id=name)
            return True
        raise elasticsearch.NotFoundError("The contact by that name does not exist in the data store")

    #List a subset of results in alphabetical order
    #   epp - entries per page
    #   page - starts at 0
    #returns a list of contact objects with results of search
    def list_contacts(self, epp, page):
        if (not isinstance(epp, int) or not isinstance(page, int)):
            raise TypeError("Arguments must be integers")
        if (epp < 1):
            raise ValueError("Must have at least one item per page")
        if (page < 0):
            raise ValueError("Page cannot index below zero")
        frm = epp*(page)
        body = {"query": {"match_all" : {}}}
        data = self.es.search(index=INDEX, doc_type='_doc', from_=frm, size=epp, body=body)
        entries = []
        for i in data['hits']['hits']:
            entry = Contact(i['_source']['name'].capitalize(), i['_source']['address'], i['_source']['phnm'], i['_source']['email'])
            entries.append(entry)
        return entries

    #Shorthand to make typing easier
    def has(self, name):
        if isinstance(name, int) or isinstance(name, float):
            raise TypeError("Must be string!")
        return self.es.exists(index=INDEX, doc_type='_doc', id=name)

