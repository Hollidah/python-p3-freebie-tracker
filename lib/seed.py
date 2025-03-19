#!/usr/bin/env python3

from models import Base, Company, Dev, Freebie
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# Database set-up
engine = create_engine("sqlite:///freebies.db")
Base.metadata.create_all(engine)     # creating database tables

# create a session
Session = sessionmaker(bind=engine)
session = Session()


# Clear existing data
session.query(Freebie).delete()
session.query(Company).delete()
session.query(Dev).delete()
session.commit()


# Companies
company1 = Company(name="Amazon", founding_year=1999)
company2 = Company(name="Meta", founding_year=2010)
company3 = Company(name="Cisco", founding_year=2000)

# Devs
dev1 = Dev(name="Leila")
dev2 = Dev(name="Jade")
dev3 = Dev(name="Jack")

# Freebies
freebie1 = Freebie(item_name="Water Bottle", value=100, dev=dev1, company=company1)
freebie2 = Freebie(item_name="Note Book", value=50, dev=dev2, company=company3)
freebie3 = Freebie(item_name="Mug", value=20, dev=dev3, company=company2)

session.add_all([company1, company2, company3, dev1, dev2, dev3, freebie1, freebie2, freebie3])
session.commit()

# Test Freebie relationship
print("Testing Freebie relationships:")
print(f"Freebie1 dev: {freebie1.dev.name}")
print(f"Freebie1 company: {freebie1.company.name}")


# Test Company relationship
print("\nTesting Company relationships:")
print(f"Amazon freebies: {[f.item_name for f in company1.freebies]}")
print(f"Amazon devs: {[d.name for d in company1.devs]}")


# Dev relationships
print("\nTesting Dev relationships:")
print(f"Leila freebies: {[f.item_name for f in dev1.freebies]}")
print(f"Leila companies: {[c.name for c in dev1.companies]}")


# freebies received by devs
print(dev1.received_one("Mug"))
print(dev3.received_one("Note Book"))


# transfer ownership of freebie
print("\nTesting give_away:")
dev1.give_away(dev2, freebie1)
session.commit()
print(freebie1.print_details())     # print details after transfer


# find oldest comapny
print("\nOldest company:")
print(Company.oldest_company(session).name)

# print all companies
print("\nCompanies:")
for company in session.query(Company).all():
    print(f"- {company.name} (Founded: {company.founding_year})")

 
 # print all freebies
print("Freebies:")
for freebie in session.query(Freebie).all():
    print(f"- {freebie.print_details()}")  

session.close() 



