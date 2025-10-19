from DBMS.DBFile import DBFile
import os
"""
Database Management Systems Programming assignment 1
Joshua Stenger
Due date 10/8/2025
Description: This is program implements a standard input version of a database management system that I am naming EQ_Database.

"""
def main():
    if 'Tables' not in os.listdir('./'):
        try:
            os.mkdir(path=os.getcwd + 'Tables')
        except Exception as e:
            print(f'Error creating Tables directory in cwd: {e}')

    dbfile = DBFile()

    print('------------------------------------------------------------------------')
    print('Welcome to the EQ_Database management system by Joshua Stenger! (Standard input version)')
    print('------------------------------------------------------------------------')

    while True:

        print('Please select one of the following options(Enter an integer responding to the option. Ex: 1):')
        print('1. Create a new table')
        print('2. Insert data into a table')
        print('3. Remove data from a table')
        print('4. Print a file/table')
        print('5. Exit EQ_Database')

        match int(input('Enter option: ')):
            case 1:
                dbfile.createTable()
            case 2:
                dbfile.insert()
            case 3:
                dbfile.delete()
            case 4:
                dbfile.printFile()
            case 5:
                dbfile.purge()
                print('Exiting EQ_Database, goodbye!')
                return
            case _:
                print('Invalid input, input a whole integer corresponding to the options. Example: 1')

if __name__ == '__main__':
    main()