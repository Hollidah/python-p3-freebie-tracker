#!/usr/bin/env python3

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'
    id =Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    founding_year = Column(Integer)

    # Relationships
    freebies = relationship('Freebie', back_populates='company')      # company freebies, backreflets Freebies access its company
    devs = relationship('Dev', secondary='freebies', back_populates='companies')    # many-to-many relationship;company is linked to devs through the freebies table


    # Giving freebies to Devs
    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)

    # Find the oldest Company
    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()


class Dev(Base):
    __tablename__ = 'devs'
    id =Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Many-to-many relationship between freebies and companies
    freebies = relationship('Freebie', back_populates='dev')
    companies = relationship('Company', secondary='freebies', back_populates='devs')


    # check if a Dev received a speficic freebies
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    # transfer freebie ownership to another dev
    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev
            return freebie
        else:
            return "You don't own this freebie."


    @property
    def companies_with_freebies(self):
        return {freebie.company for freebie in self.freebies}


class Freebie(Base):
    __tablename__ = 'freebies'
    id =Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id')) 
    dev_id = Column(Integer, ForeignKey('devs.id'))

    # relationship between the companies and devs
    company = relationship('Company', back_populates='freebies')
    dev = relationship('Dev', back_populates='freebies')

    def belongs_to(self, dev):
        return self.dev == dev

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}


    # Database setup
engine = create_engine("sqlite:///freebies.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


