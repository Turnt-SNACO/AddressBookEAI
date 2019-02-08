# AddressBookEAI
An address book RESTful API for the EAI coding challenge

* ElasitcAB.py: layer that actually interacts with Elasticsearch
* EAB_WebGUI.py: the front-end layer that will display web pages to use the ElasticAB graphically
* Populate.py: A script to fill a local Elasticsearch with dummy data for testing, is called by populate to test list function.  has dependencies of names (pip install names) and Faker (pip install Faker)
* Contact.py: Used by ElasticAB and the Unit test file for checking instance of data return types
