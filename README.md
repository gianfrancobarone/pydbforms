#PyDBforms

####What is PyDbforms? 
PyDbforms is a db forms  generator for sqlite. Basically the idea behind is to create a python library to  make GUI CRUD operations just telling to python the name of the table e the sqlite file. Ok that's enough for now. More to come!

####Current development 
Basically it's still a prototype but is working. You can use it to look at the code to got some ideas but is not ready for production. Critics, comments and suggestions are welcome !

####Quick start!
Download it from the repository and make a first test by simply modify the main.py file: put your sqlite3 database in the same directory change the database name variable 'Dbname' and table variable 'tablename' (and 'tablename2' if you want) and you are ready. Adding more table is very easy just follow the code...

Pydbforms is also smart enough to read the fk constraint related table so basically the input is a combobox if the column has a foreign key (but currently null are allowed so if you don't want to raise an error the fk column must be nullable).  





