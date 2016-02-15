__author__ = 'pangboww'
NUM_EMAIL = 1000

import csv
from faker import Faker

fake = Faker()
with open("name_list", "wb") as openfile:
    i = 0
    while True:
        name = fake.email()
        if name.find("gmail.com") == -1:
            continue

        i += 1
        print name
        openfile.write(name+"\n")

        if i == NUM_EMAIL:
            break

