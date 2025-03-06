#!/usr/bin/env python3
from models import Base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker


class Company(Base):
    __tablename__ = 'companies'
    id =Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    freebies = relationship('Freebie', back_populates='company')
    devs = relationship('Dev', secondary='freebies', back_populates='companies')

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        
    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()


class Freebie(Base):
    __tablename__ = 'freebies'
    id =Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    Company_id = Column(Integer, ForeignKey('companies.id')) 
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company = relationship('Company', back_populates='freebies')
    dev = relationship('Dev', back_populates='freebies')

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"


class Dev(Base):
    __tablename__ = 'devs'
    id =Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    freebies = relationship('Freebie', back_populates='dev')
    companies = relationship('Company', secondary='freebies', back_populates='devs')

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev
            return freebie
        else:
            return "You don't own this freebie."



# Database setup
engine = create_engine("sqlite:///freebies.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Tests
company1 = Company(name="Amazon", founding_year=1999)
company2 = Company(name="Meta", founding_year=2010)
company3 = Company(name="Cisco", founding_year=2000)

dev1 = Dev(name="Leila")
dev2 = Dev(name="Jade")
dev3 = Dev(name="Jack")

freebie1 = Freebie(item_name="Water Bottle", value=10, dev=dev1, company=company1)
freebie2 = Freebie(item_name="Note Book", value=20, dev=dev2, company=company3)
freebie3 = Freebie(item_name="Mug", value=10, dev=dev3, company=company2)


sesssion.add_all([company1, company2, company3, dev1, dev2, dev3, freebie1, freebie2, freebie3])
session.commit()

dev1.received_one(freebie1)
dev2.received_one(frebbie1)
dev3.received_one(freebie2)
dev2.received_one(freebie3)

session.commit()

# dev1.give_away(dev2, freebie)



print(freebie1.print_details())
print(dev1.received_one("Mug"))
print(dev3.received_one("Note Book"))

dev1.give_away(dev2, freebie1)
session.commit()

print(freebie1.print_details())
print(Company.oldest_company(session).name)

