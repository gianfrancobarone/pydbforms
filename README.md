#PyDBforms

####What is PyDbforms? 
PyDbforms is a db forms  generator for sqlite. Basically the idea behind is to create a python library to  make GUI CRUD operations just telling to python the name of the table e the sqlite file. Ok that's enough for now. More to come!

####Current development 
Basically it's still a prototype but is working. You can use it to look at the code to got some ideas but is not ready for production. Critics, comments and suggestions are welcome !

####Getting started!
Download it from the repository and make a first test by simply modify the main.py file: put your sqlite3 database in the same directory change the database name variable 'Dbname' and table variable 'tablename' (and 'tablename2' if you want) and you are ready. Adding more table is very easy just follow the code...

Pydbforms is also smart enough to read the fk constraint related table so basically the input is a combobox if the column has a foreign key (but currently null are not allowed so the first value from the fk column be will be selected).  

####ToDo:
1) Implent option to make table editable or not.

2) ~~Refactor files structure.~~

3) Make an exe file and let user to use the exe on windows using a definition file GUI and table.

4) Add date with calendar picker.

5) Reporting features (graphs, hystograms etc.).

6) Sql editor/Advanced mode.

7) Excel importer/exporter.

8) Formula creator (create optional columns based on formula defined in a text file, like sums, mean, range etc.).





