#!/usr/bin/env python
# -.- coding: utf-8 -.-

from sqlalchemy import or_, desc
from sqlalchemy.sql import func
from sqlalchemy.orm import backref
from sqlalchemy.dialects.mssql import BIT
from sqlalchemy import Column, Integer, String
#from sqlalchemy.types import Date
from .database import Base


class Person(Base):

    __tablename__ = 'person'
    pid = Column(Integer, primary_key=True)
    lastName = Column(String(50))
    firstName = Column(String(21))
    nameC = Column(String(20))
    nameOther = Column(String(15))
    collector = Column(BIT)

'''class Base():
    def save(self):
        if self.id == None:
            db.session.add(self)
        #else:
        #    pass
        db.session.commit()

    def delete(self):
        if self.id:
            db.session.delete(self)
            db.session.commit()'''

### Begin HAST ###
'''
RecordBasis>PreservedSpecimen
MultiMediaObject > FileURI
Gathering > DateTime
          > Agents
               > GatheringAgent
                     > Person
                         > FullName
'''

'''class Person(Base):

    __tablename__ = 'person'
    pid = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(50))
    firstName = db.Column(db.String(21))
    nameC = db.Column(db.String(20))
    nameOther = db.Column(db.String(15))
    collector = db.Column(BIT)

    @property
    def name_en(self):
        if self.lastName:
            # 有些沒有 firstName
            if self.firstName:
                return '{}, {}'.format(self.lastName, self.firstName)
            else:
                return self.lastName
        else:
            return ''

    __mapper_args__ = {'order_by': lastName}


class Hast(Base):

    #__tablename__ = 'hast'
    __tablename__ = 'vwHastDetail'

    SN = db.Column(db.Integer, primary_key=True)
    collectorID = db.Column(db.Integer, db.ForeignKey('person.pid'))
    collectNum1 = db.Column(db.Integer)
    collectNum2 = db.Column(db.String(20))
    collectorID = db.Column(db.Integer, db.ForeignKey('person.pid'))
    collectionDate = db.Column(db.DateTime)
    companion = db.Column(db.String(150))
    companionE = db.Column(db.String(150))
    WGS84Lng = db.Column(db.String(32))#DECIMAL(9,6)
    WGS84Lat = db.Column(db.String(32))#DECIMAL(8,6)
    alt = db.Column(db.Integer)
    altx = db.Column(db.Integer)

    provinceNo = db.Column(db.Integer, db.ForeignKey('province.provinceNo'))
    hsienNo = db.Column(db.Integer, db.ForeignKey('hsienCity.hsienNo'))
    townNo = db.Column(db.Integer, db.ForeignKey('hsiangTown.townNo'))
    localityID = db.Column(db.Integer)
    parkNo = db.Column(db.Integer)
    countryNo = db.Column(db.Integer, db.ForeignKey('country.countryNo'))
    additionalDesc = db.Column(db.String(255))
    additionalDescE= db.Column(db.String(255))

    collector = db.relationship('Person')
    country = db.relationship('Country')
    province = db.relationship('Province')
    hsien = db.relationship('HsienCity')
    town = db.relationship('HsiangTown')
    verifications = db.relationship('Verification')
    duplications = db.relationship('Duplication')

    verSpeciesID = db.Column(db.Integer, db.ForeignKey('vwSpecies.speciesID'))
    verGesnuID = db.Column(db.Integer, db.ForeignKey('vwGenus.genusID')) # typo 
    verFamilyID = db.Column(db.Integer, db.ForeignKey('vwFamily.familyID'))
    verSpeciesC = db.Column(db.String(255))
    verSpeciesE = db.Column(db.String(255))
    verFamilyC = db.Column(db.String(255))
    verFamilyE = db.Column(db.String(255))
    verGenusC = db.Column(db.String(255))
    verGenusE = db.Column(db.String(255))
    #verifierName = db.Column(db.String(255))

    def to_dwc(self): # DEPRICATED
        return {
            'recordedBy': self.collector.nameC if self.collector else '',
            'recordNumber': '{} {}'.format(self.collectNum1, self.collectNum2),
            'occurenceID': 'urn:catalog:hast:specimen:{}'.format(self.SN),
            'collectionID': 'a' #self.specimenOrderNum
        }

class Verification(Base):

    __tablename__ = 'verification'

    ID = db.Column(db.Integer, primary_key=True)
    SN = db.Column(db.Integer, db.ForeignKey('vwHastDetail.SN'))
    verificationNo = db.Column(db.Integer) # TODO
    verifierid = db.Column(db.Integer, db.ForeignKey('person.pid'))
    verificationDate = db.Column(db.DateTime)
    creationDate = db.Column(db.DateTime)
    speciesID = db.Column(db.Integer, db.ForeignKey('vwSpecies.speciesID'))
    genusID = db.Column(db.Integer, db.ForeignKey('vwGenus.genusID'))
    familyID = db.Column(db.Integer, db.ForeignKey('vwFamily.familyID'))

    verifier = db.relationship('Person')
    species = db.relationship('Species')
    genus = db.relationship('Genus')
    family = db.relationship('Family')

    __mapper_args__ = {'order_by': ID.desc()} # 很多第二筆 verification 都沒有日期資料


class Duplication(Base):

    __tablename__ = 'duplications'

    dupID = db.Column(db.Integer, primary_key=True)
    SN = db.Column(db.Integer, db.ForeignKey('vwHastDetail.SN'))
    dupNo = db.Column(db.Integer)


class Specimen(Base):

    __tablename__ = 'specimens'

    specimenOrderNum = db.Column(db.Integer, primary_key=True)
    dupID = db.Column(db.Integer, db.ForeignKey('duplications.dupID'))

    duplication = db.relationship('Duplication', backref=backref('specimen',uselist=False))


class Species(Base):
    __tablename__ = 'vwSpecies'

    speciesID = db.Column(db.Integer, primary_key=True) # no primary key
    speciesE = db.Column(db.String(130))
    speciesC = db.Column(db.String(60))
    genusE = db.Column(db.String(30))
    genusC = db.Column(db.String(25))
    #speciesExpr, familyID, informal, epitheN, genusE, genusC, familyE, familyC, classID, classE, classC

class Genus(Base):
    __tablename__ = 'vwGenus'

    genusID = db.Column(db.Integer, primary_key=True) # no primary key
    genusE = db.Column(db.String(30)) # 最後都有空白
    genusC = db.Column(db.String(25))
    familyID = db.Column(db.Integer, db.ForeignKey('vwFamily.familyID'))

class Family(Base):
    __tablename__ = 'vwFamily'

    familyID = db.Column(db.Integer, primary_key=True) # no primary key
    familyE = db.Column(db.String(30))
    familyC = db.Column(db.String(25))

class Country(Base):
    __tablename__ = 'country'

    countryNo = db.Column(db.Integer, primary_key=True)
    countryC = db.Column(db.String(32))
    countryE = db.Column(db.String(32))
    country = db.Column(db.String(32))

class Province(Base):
    __tablename__ = 'province'

    provinceNo = db.Column(db.Integer, primary_key=True)
    provinceC = db.Column(db.String(30))
    provinceE = db.Column(db.String(40))


class HsiangTown(Base):
    __tablename__ = 'hsiangTown'

    townNo = db.Column(db.Integer, primary_key=True)
    hsiangTownC = db.Column(db.String(30))
    hsiangTownE = db.Column(db.String(30))

class HsienCity(Base):
    __tablename__ = 'hsienCity'

    hsienNo = db.Column(db.Integer, primary_key=True)
    provinceNo = db.Column(db.Integer)
    hsienCityC = db.Column(db.String(30))
    hsienCityE = db.Column(db.String(30))'''
