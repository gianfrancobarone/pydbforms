'''
Created on 26/apr/2016

@author: tecno
'''

import sqlite3

#Use once to create test DB and table
def create_table():
    conn = sqlite3.connect('test.db')
    print "Opened database successfully";
    conn.execute('''CREATE TABLE COMPANY
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);''')
    print "Table created successfully";
    
# Return table column id, column name, column type, is not null, default value, is PK
def get_table_metadata(mDBname, mTable):
    conn = sqlite3.connect(mDBname)
    print "Opened database successfully" 
    s = "PRAGMA table_info('" + mTable + "');"
    cur = conn.cursor()    
    cur.execute(s)
    data = cur.fetchall()     
    for d in data:
        print d[0], d[1], d[2], d[3], d[4], d[5]  
    
    
get_table_metadata('test.db', 'COMPANY')
    


