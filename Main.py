from DBMS.DBFile import DBFile
"""
Main program file for my database system, which I am naming EQ_DBMS. 
I kinda of want to turn this into a self sustained project ouside of class so thats why I am giving it a name lol.

In this file I am just going to throw in a demo of the program, throwing you into a loop of creating a table and then collumns.
Inserting some values, deleting them, and then printing the file and purging the commits etc...
"""

def main():
    db_file = DBFile()

    db_file.createTable()

if __name__ == '__main__':
    main()