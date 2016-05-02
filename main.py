from Tkinter import *
from pydbforms import dataview

# Note: table names are case sensitive
tablename = 'Customers'
tablename2 = 'OrderDetails'
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
# 4. Type 'r' for record view 'g' for grid view 
# 5. Sort by column index (first column is 0) 
# 6. Editable parametr: if set to True you can make CRUD on data. 

filemenu = Menu(menubar, tearoff=0)
#filemenu.add_command(label="Record view Test Table", command=lambda: dataview.scrolled_view(root,DBname,tablename,'r',0,True))
filemenu.add_command(label="Grid view " + tablename, command=lambda: dataview.scrolled_view(root,DBname,tablename,'g',0,False))
#filemenu.add_command(label="Record view Test Table2", command=lambda: dataview.scrolled_view(root,DBname,tablename2,'r',0,True))
filemenu.add_command(label="Grid view " + tablename2, command=lambda: dataview.scrolled_view(root,DBname,tablename2,'g',0,True))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Tables", menu=filemenu)

root.config(menu=menubar)

root.mainloop()
