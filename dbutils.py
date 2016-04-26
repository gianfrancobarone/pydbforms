'''
Created on 26/apr/2016

@author: tecno
'''

import sqlite3
import tkMessageBox

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
    print "Table created successfully"
    
# Pragma return data in this order: table column id, column name, column type, is not null, default value, is PK
def get_table_metadata(mDBname, mTable, sort=0, ad='ASC'):
    try:        
        conn = sqlite3.connect(mDBname)         
        s = "PRAGMA table_info('" + mTable + "');"
        cur = conn.cursor()    
        cur.execute(s)
        data = cur.fetchall()
        col_names = []
        for d in data:
            col_names.append(str(d[1]))     
        cur.execute("select * from " + mTable + " order by " + col_names[sort] + ' ' + ad)    
        ## Get table data
        data = []
        data_number = 0
        for row in cur:
            data_number = data_number + 1
            data.append(row)
        conn.close()
        #print col_names, data        
        return col_names, data
    except Exception, err:
        tkMessageBox.showerror("Error", err) 
         
    
    
# For test
#get_table_metadata('test.db', 'COMPANY')
    


