'''
Created on Dec 29, 2012
Database connection to Raspberrypi

@author: hugo
'''

import psycopg2
import sys,time,datetime

#from datetime import timedelta

def totimestamp(dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6 

def postMessage(m):
    
    con = None
    code = "Failed"

    debug = False

    # get utc timestamp
    rightnow = time.time()
    now = datetime.datetime.utcnow()
    utc = totimestamp(now)

    try:     
        con = psycopg2.connect(database='p1db', user='hugo',password='snampook', host='127.0.0.1')
        con.autocommit = True
        cur = con.cursor()
        #cur.execute('SELECT version()')
        sql = 'insert into "p1data" (utc_timestamp,daldag,piekdag,afgenomen_vermogen,gas) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' % (utc,m['daldag'],m['piekdag'],m['afgenomen_vermogen'],m['gas']) 
        cur.execute(sql)
        #cur.commit()
        if debug:
            cur.execute("""SELECT * from p1data""")
            ver = cur.fetchall()
            print ver
        code = "Succes"
        
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e    
        sys.exit(1)
        
    finally:
        if con:
            con.close()
    return code
if __name__ == '__main__':
    

    m={}
    m['daldag'] = 0000.000
    m['piekdag'] = 0000.0000
    m['afgenomen_vermogen'] = 000.000
    m['gas']= 000.000

    postMessage(m)
