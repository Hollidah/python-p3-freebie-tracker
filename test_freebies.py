from lib.seed import session, Company, Devs, F

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

sesssion.add_all([company1, company2, company3, dev1, dev2, dev3, freebie1, freebie2, freebie3])
session.commit()

dev1.received_one(freebie1)
dev2.received_one(frebbie1)
dev3.received_one(freebie2)
dev2.received_one(freebie3)

session.commit()


print(freebie1.print_details())
print(dev1.received_one("Mug"))
print(dev3.received_one("Note Book"))

dev1.give_away(dev2, freebie1)
session.commit()

print(freebie1.print_details())
print(Company.oldest_company(session).name)

# print all companies
print("Companies:")
for commpany in session.query(Company).all():
    print(f"- {company.name} (Founded: {company.founding_year})")

 
 # print all devs
print("\nFreebies:")
for commpany in session.query(Freebie).all():
    print(f"- {freebie.print_details()}")  

session.close() 



