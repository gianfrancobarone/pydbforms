# Author: Gianfranco Barone
# Date: 2016-05-03

# Nores:
# Views is supported but they need the have editable parameter set to false or it will raise an exception
# You can use table referenced by FK keys as enum. The deafualt sorting for enum is by value, 
# if you want it rowid (FIFO) you must name the table as tablename + '_EBRI'.
# If you want some columns being not visible add '_NV' to the column name.
# In order to check the correct value format you can use the SQLITE builtin 'Check' function or a Trigger.

from Tkinter import *
from pydbforms import dataview

# Note: table names are case sensitive
tablename = 'Customers'
tablename2 = 'OrderDetails'
report = 'report_view'

DBname='testdb.db'

root = Tk()
root.title('Pyforms')
root.configure(background='dark slate gray')
menubar = Menu(root)   

# create a pulldown menu, and add it to the menu bar
# Parameters to pass to scrolled_view:
# 1. Root app 
# 2. database filename and path 
# 3. Table name 
# 4. Type 'r' for record view 'g' for grid view # 5. Sort by column index (first column is 0) 
# 6. Editable parametr: if set to True you can make CRUD on data. 

filemenu = Menu(menubar, tearoff=0)
#filemenu.add_command(label="Record view Test Table", command=lambda: dataview.scrolled_view(root,DBname,tablename,'r',0,True))
filemenu.add_command(label="Grid view " + tablename, command=lambda: dataview.scrolled_view(root,DBname,tablename,'g',0,False))
#filemenu.add_command(label="Record view Test Table2", command=lambda: dataview.scrolled_view(root,DBname,tablename2,'r',0,True))
filemenu.add_command(label="Grid view " + tablename2, command=lambda: dataview.scrolled_view(root,DBname,tablename2,'g',0,True))
filemenu.add_command(label="Grid view " + report, command=lambda: dataview.scrolled_view(root,DBname,report,'g',2,False))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Tables", menu=filemenu)

root.config(menu=menubar)

root.mainloop()
