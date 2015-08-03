'''
Created on Dec 29, 2012
Database connection to Raspberrypi

@author: hugo
'''

import psycopg2
import sys

con = None

try:     
    con = psycopg2.connect(database='p1db', user='hugo',password='snampook', host='127.0.0.1') 
    cur = con.cursor()
    #cur.execute('SELECT version()')          
    cur.execute("""SELECT datname from pg_database""")
    ver = cur.fetchall()
    print ver    
    
except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
    
finally:
    if con:
        con.close()
