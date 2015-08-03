'''
Created on Jan 16, 2014

@author: hugo
'''

from sqlalchemy import *
import json
from flask import *

SQLALCHEMY_DATABASE_URI = 'postgresql://hugo:snampook@raspberrypi/p1db'
SQLALCHEMY_ECHO = True

db = create_engine(SQLALCHEMY_DATABASE_URI)

sql = """
select
EXTRACT(HOUR FROM to_timestamp(utc_timestamp)),
avg(afgenomen_vermogen) as a_av,
stddev(afgenomen_vermogen) as st_av
from p1data
group by
EXTRACT(HOUR FROM to_timestamp(utc_timestamp));"""

result = db.engine.execute(sql)

for row in result:
    dict = [{row.keys()[r]:row.values()[r]} for r in range(len(row))]
    print json.dumps([{row.keys()[r]:row.values()[r]} for r in range(len(row))])
    
