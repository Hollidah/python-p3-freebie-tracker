print("Loading models.py from:", __file__)

from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    founding_year = Column(Integer())


    # Relationship between freebies and comapany
    freebies = relationship('Freebie', back_populates='company')
    devs = relationship('Dev', secondary='freebies', back_populates='companies', overlaps='freebies' )    # many-to-many relationship;company is linked to devs through the freebies table


    # Giving freebies to Devs
    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add (freebie)
        return freebie


    # Finding the oldest company
    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String(), nullable=False)

    # Many-to-many relationships between Devs and Companies 
    freebies = relationship('Freebie', back_populates='dev')
    companies = relationship('Company', secondary='freebies', back_populates='devs', overlaps='freebies')


    # Check if Dev received a specific freebie
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    # Transfer ownwership of freebie to anaother Dev
    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev
            return freebie
        else:
            return "You don't own this freebie."

    # Track which companies the dev has received freebies from
    @property
    def companies_with_freebies(self):
        return {freebie.company for freebie in self.freebies}

    def __repr__(self):
        return f'<Dev {self.name}>'


class Freebie(Base):
    __tablename__ = 'freebies'
    id =Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id')) 
    dev_id = Column(Integer, ForeignKey('devs.id'))

    # Relationship between the companies and devs
    company = relationship('Company', back_populates='freebies', overlaps='companies,devs')
    dev = relationship('Dev', back_populates='freebies', overlaps='companies,devs')


    # check if freebie belongs to a specific dev
    def belongs_to(self, dev):
        return self.dev == dev

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"




