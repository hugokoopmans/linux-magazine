'''
Created on Jan 5, 2014

@author: hugo
'''
import json
import datetime,time

from flask import Blueprint, render_template, url_for
from .models import db,P1data

# create a blueprint
rpiapp = Blueprint("rpiapp", __name__)

# generic timestamp function
def totimestamp(dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6

@rpiapp.route('/')
def home():
    return render_template('home.html')

@rpiapp.route('/about')
def about():
  return render_template('about.html')

@rpiapp.route('/p1')
def p1():
  return render_template('p1.html')
  
@rpiapp.route("/data")
@rpiapp.route("/data/<int:interval>")
def data(interval = 86400):
    """
    On request, this returns a list of the last now to now - interval data points.

    :param interval: (optional) default : last 24 hours
        The interval between now and now - interval to return.

    :returns data:
        A JSON string of ``ndata`` data points.

    """
    # dump db result in json P1data.query.get(ndata)
    #result = P1data.query.get(ndata)
    #result = P1data.query.count()
    #interval = 86400 # 24 uur = 24 x 3600 = 
    now = datetime.datetime.utcnow()
    utc = totimestamp(now)
#    result = P1data.query.filter(P1data.utc_timestamp > utc - interval, P1data.utc_timestamp < utc)
    result = P1data.query.filter(P1data.utc_timestamp > utc - interval, P1data.utc_timestamp < utc)
    d=[]
    for row in result.all():
        r={}
        r['utc_timestamp'] = row.utc_timestamp
        r['afgenomen_vermogen'] = row.afgenomen_vermogen
        d.append(r)

    return json.dumps(d)


@rpiapp.route("/data/a24h")
@rpiapp.route("/data/a24h/<int:dow>")
def data_24h(dow = 0):
    """
    On request, this returns an aggregate of the value group by hour of day.

    :param dow: (optional)
        The day of the week to return.

    :returns data:
        A JSON string of ``avgerage and standard dev over 24 hours`` data points.

    """
    now = datetime.datetime.utcnow()
    utc = totimestamp(now)
#    result = P1data.query.filter(P1data.utc_timestamp > utc - interval, P1data.utc_timestamp < utc)
    result = P1data.query.filter(P1data.utc_timestamp > utc - interval, P1data.utc_timestamp < utc)
    d=[]
    for row in result.all():
        r={}
        r['utc_timestamp'] = row.utc_timestamp
        r['afgenomen_vermogen'] = row.afgenomen_vermogen
        d.append(r)

    return json.dumps(d)
