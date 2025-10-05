import os
import logging
import logging.config

class DBFile:
    def __init__(self):
        logging.config.fileConfig('../logger/logger.conf')
        self._logger = logging.getLogger('FileLogger')

    def __str__(self):
        return 'Class for working with tables in the EQ_Database system.'
    
    def createTable(self):
        """
        Function that takes input from a user wanting to created a new table.
        These events happen:
        1. The user is prompted to enter a name for the table.
        2. The user is then put in a loop of asking for collumns and their lengths that pertain to that table until they type q to quit as the length or name.
        3. We then add the table to the main table file.
        """
            
        table_name = input('Enter table name: ')
        print('You will be prompted to insert collumns')
        print('When you are finished entering collumns type q in as the next collumns length.')
        
        # Collumns is a list containing tuples, the tuples have the collumn name and then the length of values/strings
        collumns = []
        
        try:
            with open('../Tables/dbFiles.db','a') as f:
                while True:
                    collumn_name = input('Enter collumn name: ')
                    length = input(f'Enter the length of {collumn_name}: ')
                    f.write(f'{table_name}  {collumn_name}  {length} \n')

                    if length == 'q':
                        self._logger.debug(f'User added a new table {table_name}, length of {table_name} = {len(collumns)}')
                        break
                    else:
                        collumns.append((collumn_name,length))
            
            with open(f'../Tables/{table_name}','a') as t:
                table_str = ''
                for tup in collumns:
                    x,y = tup
                    if table_str[-1] is ' ' or table_str is '' :
                        table_str += f'{x}({y})'
                    else:
                        table_str += ' ' + f'{x}({y})'
        except Exception as e:
            self._logger.fatal('User encountered an error while adding table: ',e)            

            

