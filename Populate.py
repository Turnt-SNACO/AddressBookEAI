# Author: James Anderson
# EAI Coding Challenge: Address Book

from faker import Faker
import names
from ElasticAB import ElasticAB
import random

eab = ElasticAB()
fake=Faker()

def fake_number():
    a = random.randint(100,999)
    b = random.randint(100,999)
    c = random.randint(1000,9999)
    output = "{0}-{1}-{2}".format(a,b,c)
    return output

for i in range(100):
    print(i)
    fake_email = "{0}@{1}.com".format(names.get_first_name(), names.get_last_name())
    eab.add_contact(fake.name(), fake.address(), fake_number(), fake_email)
print('done')