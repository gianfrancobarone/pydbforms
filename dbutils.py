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
        pk_col = ''
        #col_types = []
        for d in data:
            col_names.append(str(d[1]))
            if (str(d[5]) == '1'):
                pk_col = str(d[1])                     
        cur.execute("select * from " + mTable + " order by " + col_names[sort] + ' ' + ad)    
        ## Get table data
        data = []
        data_number = 0
        for row in cur:
            data_number = data_number + 1
            data.append(row)
        conn.close()                                 
        return col_names, data, pk_col
    except Exception, err:
        tkMessageBox.showerror("Error", err) 
        
# Return foreing table, column with fk, foreing column, values
def get_table_fk(mDBname, mTable):
    conn = sqlite3.connect(mDBname)      
    #s = "PRAGMA foreign_keys = ON;" 
    fk_cols = []    
    cur = conn.cursor()    
    s = "PRAGMA foreign_key_list('" + mTable + "');"
    cur.execute(s)
    data = cur.fetchall()
    for d in data:
        row = [str(d[2]),str(d[3]),str(d[4])]
        s = 'select ' + row[2] + ' from ' + row[0]
        cur.execute(s)
        rows = cur.fetchall()
        for r in rows:            
            row.append(str(r))   
        fk_cols.append(row)
    conn.close()
    return fk_cols
        
def create(mDBname,tablename,cols,values):           
    conn = sqlite3.connect(mDBname)
    curs = conn.cursor() 
    # String construction   
    string1 = "insert into " + tablename + " ("        
    for col in cols:
        string1 = string1 + col + ","           
    string1 = string1[:-1] + ") "
    i = 0    
    string2 = "values ("        
    for value in values:        
        value = "'" + values[i] + "'"    
        if values[i] == '': value = 'null'           
        string2 = string2 + value + ","
        i = i + 1
    string2 = string2[:-1] + ")" 
    string = string1 + string2 + ';'
    print string                    
    curs.execute(string)        
    conn.commit()  
    curs.close()
    conn.close()
    
def update(mDBname, tablename, cols, new_values, old_values):    
    conn = sqlite3.connect(mDBname)
    curs = conn.cursor() 
    # String construction       
    string = "update " + tablename + " set"
    for i in range(0,len(cols)):
        string = string + " " + cols[i] + " = " 
        value = "'" + new_values[i] + "'"    
        if new_values[i] == '': value = 'null'  
        string = string + value + ","
    string = string[:-1] + " where "         
    for i in range(0,len(cols)):
        string = string + " " + cols[i] + " = " 
        value = "'" + str(old_values[i]) + "'"    
        if old_values[i] == '': 
            string = string[:-2]
            value = "is null"  
        string = string + value + " AND "              
    string = string[:-4] + ';'    
    curs.execute(string)    
    conn.commit()  
    curs.close()
    conn.close()
    
    
def delete(mDBname, tablename,pkcol,value):    
    conn = sqlite3.connect(mDBname)
    curs = conn.cursor() 
    string = 'delete from ' + tablename + ' where ' + str(pkcol) + ' = ' + str(value) + ';'    
    curs.execute(string)    
    conn.commit()  
    curs.close()
    conn.close()
    conn.close
         
    
    
# For test
#get_table_metadata('testdb.db', 'Orders')
get_table_fk('testdb.db', 'OrderDetails')
    


