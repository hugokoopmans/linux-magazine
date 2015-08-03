'''
Created on Jan 2, 2014
here we declare the database model
@author: hugo
'''

import datetime,time

from flask.ext.sqlalchemy import SQLAlchemy

# generic timestamp function
def totimestamp(dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6

db = SQLAlchemy()
    
class P1data(db.Model):
    """    
    utc_timestamp integer  
    daldag real  
    piekdag real
    dalterug real  
    piekterug real  
    gas real  
    afgenomen_vermogen real  
    teruggeleverde_vermogen real
    """  
    utc_timestamp = db.Column(db.Integer, primary_key=True)
    daldag = db.Column(db.REAL())
    piekdag = db.Column(db.REAL())
    gas = db.Column(db.REAL())
    afgenomen_vermogen = db.Column(db.REAL())

    def __init__(self, utc_timestamp, daldag, piekdag, gas, afgenomen_vermogen):
        self.utc_timestamp = utc_timestamp
        self.daldag = daldag
        self.piekdag = piekdag
        self.gas = gas
        self.afgenomen_vermogen = afgenomen_vermogen

    def __repr__(self):
        return '<UTC_timestamp %r>' % self.utc_timestamp
    
    
    
