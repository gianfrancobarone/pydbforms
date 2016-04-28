from Tkinter import *
import tkMessageBox
import tkFileDialog
import ttk
import dbutils

buttons = {} 
cols = {}
sort = 0
record = 0
ad = 'DESC'
root = ''
tablename_1 = ''
dbname_1 = ''
searchbox = {}
search = ''
tabledata = []

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
    
def grid_view(master_frame, mTable, mDBname):       
    table = dbutils.get_table_metadata(mDBname, mTable, sort, ad)   
    col_names = table[0]   
    rows = table[1]        
    entry = {}   
    label = {}
    global buttons 
    buttons.clear() 
    button_num = 0
    global cols
    global searchbox  
    global search
    global tabledata           
    cols_num = 0
    l = 0    
    master_frame.grid(row=0,column = 0, sticky = S) 
    button_frame = Frame(master_frame, bg = 'dark slate gray') 
    frame = Frame(master_frame, bg = 'dark slate gray')
    button_frame.grid(row=0,column=0, stick = NW) 
    frame.grid(row=1,column=0, stick = N)    
    b = Button(button_frame, text='Add Record', bd=1, bg = 'dark slate gray', fg = 'white')
    b.grid(row=1, column=l+1, sticky=W, padx=5, pady=15)
    b.bind( "<Button-1>", new_record)    
    b = Button(button_frame, text='Search', bd=1, bg = 'dark slate gray', fg = 'white')
    b.grid(row=1, column=l+4, sticky=W , padx=(5,2))
    b.bind( "<Button-1>", filter_records)
    e = Entry(button_frame, bg = 'black', fg = 'white', insertbackground='white')
    e.grid(row=1, column=l+5, sticky=W)
    searchbox['search'] = e  
    b = Button(button_frame, text='Export to CSV', bd=1, bg = 'dark slate gray', fg = 'white')
    b.grid(row=1, column=l+3, sticky=W, padx=5)
    b.bind( "<Button-1>", make_CVS)     
    for name in col_names:
        b = Button(frame, text=name, bd=0,  bg = 'dark slate gray', fg = 'white', relief='raised')
        b.grid(row=3, column=l+1, sticky=W)
        cols[b] = cols_num
        cols_num += 1
        label[name] = b        
        l += 1   
        b.bind("<Button-1>", sort_by)              
    r = 0  
    #Rows start rs
    rs = 4 
    filtered_rows = []  
    if len(search) < 1:
        filtered_rows = rows
    else:
        for rw in rows:           
            for item in rw:
                if search.lower() in (str(item).lower()):                    
                    filtered_rows.append(rw)  
                    break                                  
    tabledata = filtered_rows                   
    for row in filtered_rows:                               
        b = Button(frame, text= r+1, bg = 'dark slate gray', fg = 'white')        
        b.grid(row=r+rs, column=0, sticky = W, padx = 2)         
        buttons[b] = button_num        
        button_num += 1
        b.bind( "<Button-1>", get_record)               
        c = 0      
        for col in row:          
            e = Entry(frame, bg='black', fg='white', readonlybackground='black')
            e.grid(row=r+rs, column=c+1, padx=2)
            entry[row] = e
            if filtered_rows[r][c] == None:
                e.insert(0,'')
            else:
                e.insert(0,filtered_rows[r][c]) 
            e.configure(state='readonly')                      
            c = c + 1
        r = r + 1
        
def record_view(frame, mTable, mDBname, record=0): 
    global ad     
    #if ad == 'DESC': ad = 'ASC'
    #else: ad = 'DESC'   
    table = dbutils.get_table_metadata(mDBname, mTable, sort, ad)         
    #table = dbutils.get_table_metadata(mDBname, mTable)        
    col_names = table[0]      
    rows = table[1] 
    pk = table[2]   
    row_num = len(rows)          
    names = col_names
    entry = {}
    box = {}
    label = {}
    i = 0     
    fk_columns, fk_values = dbutils.get_table_fk(mDBname, mTable)    
    for name in names:
        try:            
            idx = fk_columns.index(name)  
            value = StringVar()          
            e = ttk.Combobox(frame, textvariable=value, state='readonly')
            e['values'] = fk_values[idx]
            e.current(0)            
            e.grid(row=i, column=2, columnspan=3, sticky=W, padx=25)
            box[name] = e
        except:                    
            e = Entry(frame)
            e.grid(row=i, column=1, columnspan=3)
            entry[name] = e                
            if (rows[record][i] == None) or (record == -1): 
                e.insert(0,'')
            else:
                e.insert(0,rows[record][i])
            if (pk == name):
                e.configure(state='readonly')        
        lb = Label(frame, text=name, bg = 'dark slate gray', fg = 'white')
        lb.grid(row=i, column=0, sticky=W, pady = 5, padx = 5)
        label[name] = lb        
        i += 1

    def forward():        
        if record < row_num - 1: 
            record_view(frame,mTable, mDBname,1+record)
        
    def back():
        if record > 0: 
            record_view(frame,mTable, mDBname, record-1)
        
    def create():
        try:
            cols = []
            values = []                
            for name in names:
                if (pk <> name):
                    if (name in fk_columns):
                        cols.append(name)
                        values.append(box[name].get())
                    else:                        
                        cols.append(name)
                        values.append(entry[name].get())                                    
            dbutils.create(mDBname, mTable,cols,values)   
            tkMessageBox.showinfo("New record", "Record created") 
            scrolled_view(root,mDBname,mTable,'g',0)           
        except Exception, err:
            tkMessageBox.showerror("Error", err) 
        
        
    def update():
        try:
            cols = []
            new_values = []
            old_values = []
            i = 0
            for name in names:
                if (name in fk_columns):
                    cols.append(name)
                    new_values.append(box[name].get())
                else:                        
                    cols.append(name)
                    new_values.append(entry[name].get())                
                if rows[record][i] == None:
                    old_values.append('')
                else:
                    old_values.append(rows[record][i]) 
                i = i + 1              
            dbutils.update(mDBname, mTable, cols, new_values, old_values) 
            tkMessageBox.showinfo("Update", "Record updated")
            scrolled_view(root,mDBname,mTable,'g',0)            
        except Exception, err:
            tkMessageBox.showerror("Error", err)       
        
        
    def delete():
        try:                            
            for name in names:
                if (pk == name):
                    pkcol = name
                    value = entry[name].get()            
            dbutils.delete(mDBname, mTable, pkcol, value)            
            tkMessageBox.showinfo("Delete record", "Record deleted")
            scrolled_view(root,mDBname,mTable,'g',0)
        except Exception, err:
            tkMessageBox.showerror("Error", err)   
            
    if (record == -1):           
        b_create = Button(frame, text="Save", command=create, width = 8)
        b_create.grid(row=i+2, column =1, sticky = N, pady=20)       
        
    else:
        b_avanti = Button(frame, text="->", command=forward)
        b_avanti.grid(row=i, column = 3, sticky = W)
        b_indietro = Button(frame, text="<-", command=back)
        b_indietro.grid(row=i, column = 2, sticky = E)              
        b_update = Button(frame, text="Update", command=update, width = 8)
        b_update.grid(row=i+2, column =2, sticky = N, pady=20)
        b_delete = Button(frame, text="Delete", command=delete, width = 8)
        b_delete.grid(row=i+2, column =3, sticky = N, pady=20)       
        
def scrolled_view(main, dbname, tablename, t, record):
    
    def on_mousewheel(event):
        canvas.yview_scroll(-1*(event.delta/120), "units")
        
    global root
    global tablename_1
    global dbname_1
    root = main    
    tablename_1 = tablename
    dbname_1 = dbname
    vscrollbar = AutoScrollbar(root)
    vscrollbar.grid(row=0, column=1, sticky=N+S)
    hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
    hscrollbar.grid(row=1, column=0, sticky=E+W)
    
    canvas = Canvas(root, bg = 'dark slate gray', 
                yscrollcommand=vscrollbar.set,
                xscrollcommand=hscrollbar.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    
    canvas.bind_all("<MouseWheel>", on_mousewheel)   

    vscrollbar.config(command=canvas.yview)
    hscrollbar.config(command=canvas.xview)

    # make the canvas expandable
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    #
    # create canvas contents

    frame = Frame(canvas, bg = 'dark slate gray')
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(1, weight=1)
    
    if t == 'r': record_view(frame,tablename, dbname, record)
    if t == 'g': grid_view(frame,tablename, dbname)
    
    canvas.create_window(0, 0, anchor=NW, window=frame)

    frame.update_idletasks()

    canvas.config(scrollregion=canvas.bbox("all"))
    
def get_record(event):    
    ## free up memory 
    for item in root.grid_slaves():
        item.destroy()       
    global buttons    
    record = buttons[event.widget]       
    scrolled_view(root,dbname_1, tablename_1,'r', record)
    
def new_record(event):
    ## free up memory 
    for item in root.grid_slaves():
        item.destroy()          
    scrolled_view(root,dbname_1, tablename_1,'r', -1)
    
def sort_by(event):
    ## free up memory 
    for item in root.grid_slaves():
        item.destroy() 
    global cols    
    global sort      
    sort = cols[event.widget]  
    global ad     
    if ad == 'DESC': ad = 'ASC'
    else: ad = 'DESC'             
    scrolled_view(root,dbname_1, tablename_1,'g',sort)
    
def filter_records(event):
    global searchbox 
    global search
    ### Set filter
    search = searchbox['search'].get()
    ## free up memory 
    for item in root.grid_slaves():
        item.destroy() 
    ### Recreate grid with filter if exist               
    scrolled_view(root,dbname_1, tablename_1,'g',0)
    
def make_CVS(event):
    f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".csv")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return 
    cvs = ''
    for row in tabledata:
        for col in row:
            cvs = cvs + str(col) + ','
        cvs=cvs[:-1] + '\n'    
    f.write(cvs)
    f.close() # `()` was missing.
    
    


