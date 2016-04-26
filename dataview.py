from Tkinter import *
import tkMessageBox
import dbutils

buttons = {} 
cols = {}
sort = 0
record = 0
ad = 'DESC'
root = ''
tablename_1 = ''

class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError, "cannot use pack with this widget"
    def place(self, **kw):
        raise TclError, "cannot use place with this widget"
    
def grid_view(frame, mTable, mDBname):     
    global ad     
    if ad == 'DESC': ad = 'ASC'
    else: ad = 'DESC'   
    table = dbutils.get_table_metadata(mDBname, mTable, sort, ad)     
    #col_number = table[0]
    col_names = table[0]
    #col_extensions =table[2]
    #row_num = table[3]
    rows = table[1]        
    entry = {}   
    label = {}
    global buttons     
    button_num = 0
    global cols
    cols_num = 0
    l = 0
    for name in col_names:
        b = Button(frame, text=name, bd=0)
        b.grid(row=0, column=l+1, sticky=W)
        cols[b] = cols_num
        cols_num += 1
        label[name] = b
        l += 1   
        b.bind("<Button-1>", sort_by)              
    r = 0
    for row in rows:                        
        b = Button(frame, text=r+1)        
        b.grid(row=r+1, column=0, sticky = W, padx = 2)         
        buttons[b] = button_num
        button_num += 1
        b.bind( "<Button-1>", get_record)               
        c = 0      
        for col in row:          
            e = Entry(frame)
            e.grid(row=r+1, column=c+1)
            entry[row] = e
            if rows[r][c] == None:
                e.insert(0,'')
            else:
                e.insert(0,rows[r][c])                       
            c = c + 1
        r = r + 1
         
def record_view(frame, tablename, record=0):        
    table = connection.Get_table(tablename,sort,ad) 
    col_number = table[0]
    col_names = table[1]
    col_extensions =table[2]    
    row_num = table[3]
    rows = table[4] 
    col_type = table[5] 
    fk_col = table[6]        
    names = col_names
    entry = {}
    label = {}
    i = 0    
    for name in names:
        e = Entry(frame)
        e.grid(row=i, column=1, columnspan=3)
        entry[name] = e                
        if rows[record][i] == None: 
            e.insert(0,'')
        else:
            e.insert(0,rows[record][i])        
        lb = Label(frame, text=name, pady = 5)
        lb.grid(row=i, column=0, sticky=W)
        label[name] = lb
        print name, fk_col
        for fk in fk_col:
            print fk
        if name in fk_col:
            b = Button(frame, text = "...", pady = 5)
            b.grid(row=i,column=2, sticky=E)
        ##b.bind( "<Button-1>", print i)   
        i += 1

    def forward():        
        if record < row_num - 1: 
            record_view(frame,tablename,1+record)
        
    def back():
        if record > 0: 
            record_view(frame,tablename,record-1)
        
    def create():
        try:
            cols = []
            values = []                
            for name in names:
                cols.append(name)
                values.append(entry[name].get())            
            connection.create(tablename,cols,values, col_type)   
            tkMessageBox.showinfo("New record", "Record created")            
        except Exception, err:
            tkMessageBox.showerror("Error", err) 
        
        
    def update():
        try:
            cols = []
            new_values = []
            old_values = []
            i = 0
            for name in names:
                cols.append(name)
                new_values.append(entry[name].get())
                if rows[record][i] == None:
                    old_values.append('')
                else:
                    old_values.append(rows[record][i]) 
                i = i + 1              
            connection.update(tablename, cols, new_values, old_values, col_type) 
            tkMessageBox.showinfo("Update", "Record updated")            
        except Exception, err:
            tkMessageBox.showerror("Error", err)       
        
        
    def delete():
        try:
            cols = []
            values = []                
            for name in names:
                cols.append(name)
                values.append(entry[name].get())            
            connection.delete(tablename,cols,values, col_type)
            forward()
            back()
            tkMessageBox.showinfo("Delete record", "Record deleted")
        except Exception, err:
            tkMessageBox.showerror("Error", err)       

    b_avanti = Button(frame, text="->", command=forward)
    b_avanti.grid(row=i, column = 3, sticky = W)
    b_indietro = Button(frame, text="<-", command=back)
    b_indietro.grid(row=i, column = 2, sticky = E)
    
    space = Label(frame, text='', pady = 5)
    space.grid(row=i+1, column = 0, sticky= W)   
    b_create = Button(frame, text="New", command=create, width = 8)
    b_create.grid(row=i+2, column =1, sticky = N)
    b_update = Button(frame, text="Update", command=update, width = 8)
    b_update.grid(row=i+2, column =2, sticky = N)
    b_delete = Button(frame, text="Delete", command=delete, width = 8)
    b_delete.grid(row=i+2, column =3, sticky = N)   
    
def scrolled_view(main, dbname, tablename, type, record):
    global root
    global tablename_1
    root = main    
    tablename_1 = tablename
    vscrollbar = AutoScrollbar(root)
    vscrollbar.grid(row=0, column=1, sticky=N+S)
    hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
    hscrollbar.grid(row=1, column=0, sticky=E+W)
    
    canvas = Canvas(root,
                yscrollcommand=vscrollbar.set,
                xscrollcommand=hscrollbar.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)

    vscrollbar.config(command=canvas.yview)
    hscrollbar.config(command=canvas.xview)

    # make the canvas expandable
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    #
    # create canvas contents

    frame = Frame(canvas)
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(1, weight=1)
    
    if type == 'r': record_view(frame,tablename, dbname, record)
    if type == 'g': grid_view(frame,tablename, dbname)
    
    canvas.create_window(0, 0, anchor=NW, window=frame)

    frame.update_idletasks()

    canvas.config(scrollregion=canvas.bbox("all"))
    
def get_record(event):    
    ## free up memory 
    for item in root.grid_slaves():
        item.destroy()       
    global buttons    
    record = buttons[event.widget]    
    scrolled_view(root,tablename_1,'r', record)
    
def sort_by(event):
    ## free up memory 
    for item in root.grid_slaves():
        item.destroy() 
    global cols    
    global sort
    sort = cols[event.widget]              
    scrolled_view(root,tablename_1,'g',sort)
    


