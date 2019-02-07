from faker import Faker
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

for i in range(10000):
    print(i)
    eab.add_contact(fake.name(), fake.address(), fake_number())
print('done')