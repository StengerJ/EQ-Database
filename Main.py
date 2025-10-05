from DBMS.DBFile import DBFile
from logger.LoggerSetup import setup_logger

"""
Database Management Systems Programming assignment 1
Joshua Stenger
Due date 10/8/2025
Description: This is program implements a standard input version of a database management system that I am naming EQ_Database.
"""
def main():
    
    setup_logger()
    dbfile = DBFile()

    while True:
        print('------------------------------------------------------------------------')
        print('Welcome to the EQ_Database management system by Joshua Stenger! (Standard input version)')
        print('------------------------------------------------------------------------')

        print('Please select one of the following options(Enter an integer responding to the option. Ex: 1):')
        print('1. Create a new table')
        print('2. Insert data into a table')
        print('3. Remove data from a table')
        print('4. Query a table')
        print('5. Exit EQ_Database')

        match int(input('Enter option: ')):
            case 1:
                dbfile.createTable()
            case 2:
                print('WARNING: If your input is longer than the allocated length for that collumn, data will be truncated.')
            case 3:
                print('Remove data from a table - Not yet implemented')
            case 4:
                print('Query a table - Not yet implemented')
            case 5:
                print('Exiting EQ_Database, goodbye!')
                break
            case _:
                print('Invalid input, input a whole integer corresponding to the options. Example: 1')

if __name__ == '__main__':
    main()