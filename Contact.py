# Author: James Anderson
# EAI Coding Challenge: Address Book

#A container for contact information
class Contact:
    def __init__(self, name, address='', phone_number='', email_address=''):
        self.name = name
        self.address = address
        self.email_address = email_address
        self.phone_number = phone_number
