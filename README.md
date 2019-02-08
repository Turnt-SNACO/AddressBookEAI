# AddressBookEAI
An address book RESTful API for the EAI coding challenge

To use the RESTful API first edit the eab.config file to hold the host and port data. The default is localhost and 9200. Once running the API will respond to curl or other http requests as specified.

* EAB_Server.py: the RESTful API for the Elasticsearch Address Book
* ElasitcAB.py: layer that actually interacts with Elasticsearch
* Contact.py: Used by ElasticAB and the Unit test file for checking instance of data return types
* Populate.py: A script to fill a local Elasticsearch with dummy data for testing, is called by populate to test list function.  has dependencies of names (pip install names) and Faker (pip install Faker)
* EAB_UnitTest.py: contains a handful of unit tests for ElasticAB.py

I also made a web interface that can perform all the same tasks as the EAB_Server. In this, the host and port can be defined on the landing page. This, however, does not utilize all the VERBs as it should for a RESTful API.

* EAB_WebGUI.py: the front-end layer that will display web pages to use the ElasticAB graphically
* templates: holds the html files for the WebGUI.

