import os
import logging
import re
class DBFile:
    def __init__(self,argDBFilePath='Tables/dbFiles.db'):
        self._path = argDBFilePath
        self._logger = logging.getLogger('FileLogger')

        if not os.path.exists(self._path):
            try:
                with open(self._path,'x') as f:
                    f.write('FILE_NAME COLUMN_NAME COLUMN_SIZE \n')
                    self._logger.info(f'Main table was not created, created it at this path: {self._path}')
            except Exception as e:
                self._logger.fatal(f'Error creating dbFiles.db: {e}')
        else:
            self._logger.info('dbFiles.db already exists from previous run.')
            

    def __str__(self):
        return 'Class for working with tables in the EQ_Database system.'
    
    def createTable(self):
        """
        Function that allows a user to create a new table.
        These events happen:
        1. The user is prompted to enter a table name.
        2. The program checks to see if the table already exists, if so it returns
        3. The user is prompted to enter collumn names and lengths until they choose to stop.
        4. The table file is created in Tables/<name>.db with the collumn definitions.
        5. Appropriate logging is done throughout the process.
        """
            
        table_name = input('Enter table name: ')

        # if table already exists, return
        if os.path.exists(f'Tables/{table_name.upper()}.db'):
            print('Table already exists, please choose another name or insert into that table.')
            self._logger.warning(f'User attempted to create a table that already exists: {table_name()}')
            return
        print('You will be prompted to insert collumns')
        print('When you are finished entering collumns type anything but an number in a the length of your next collumn.')
        
        # Collumns is a list containing tuples, the tuples have the collumn name and then the length of values/strings
        collumns = []
        
        """ This is just a note to myself/sudocode I want to keep for later
        Try to make the table name all caps, open the file in append mode, take input.
        If the length is not a number break from the loop.
        Then create the table file in Tables/<name>.db
        Do some very basic string manipulation to get the collumns into format.
        Write the collumns to the file.
        """
        try:
            table_name = table_name.upper()
            with open(self._path,'a') as f:
                while True:
                    collumn_name = input('Enter collumn name: ')
                    length = input(f'Enter the length of {collumn_name.capitalize()}: ')

                    if not re.match(r'^\d+$', length):
                        self._logger.debug(f'User added a new table {table_name}, length of {table_name} = {len(collumns)}')
                        break
                    else:
                        # use the pipe as a delimiter
                        f.write(f'{table_name}|{collumn_name}|{length} \n')
                        collumns.append((collumn_name,length))
            
            with open(f'Tables/{table_name}.db','a') as t:
                table_str = ''
                for tup in collumns:
                    x,y = tup
                    if len(table_str) == 0:
                        table_str += f'{x}({y})'
                    else:
                        table_str += ' ' + f'{x}({y})'
                
                t.write(table_str)
                self._logger.info(f'Created new table file at Tables/{table_name}.db with collumns: {table_str}')
        except Exception as e:
            self._logger.fatal(f'User encountered an error while adding table: {e}')            

    def insert(self):
        """
        Functiojn that allows a user to insert data into an existing table.
        These events happen:
        1. The user is prompted to enter the table name they wish to insert into.
        2. The program checks to see if the table exists, if not it returns.
        3. The program reads the collumn definitions from the table file.
        4. The user is prompted to enter data for each collumn, with truncation or padding as needed.
        5. The data is appended to the table file.
        6. The user is asked if they wish to insert more data, if not the function returns.
        7. Appropriate logging is done throughout the process.
        """
        table_name = input('Enter File Name: ').upper()
        table_path = f'Tables/{table_name}.db'

        if not os.path.exists(table_path):
            print('Table does not exist, please create it first.')
            self._logger.warning(f'User attempted to insert into non-existent table: {table_name}')
            return

        try:
            # read the column definitions from the table file
            with open(table_path, 'r') as f:
                header = f.readline().strip()
                if not header:
                    print("Table has no defined columns.")
                    self._logger.error(f'Table {table_name} has an empty header.')
                    return

            # seperate the definitions into column names and sizes using regex 
            columns = []
            for col_def in header.split(' '):
                match = re.match(r'(\w+)\((\d+)\)', col_def)
                if match:
                    collumn_name, collumn_size = match.groups()
                    columns.append((collumn_name, int(collumn_size)))

            if not columns:
                print("No valid columns found in header.")
                return

            # insert the data into the table
            while True:
                rows_array = []
                for collumn_name, collumn_size in columns:
                    value = input(f"{collumn_name}: ").strip()
                    if len(value) > collumn_size:
                        value = value[:collumn_size] # if users entry is too long, truncate
                    if len(value) < collumn_size:
                        value = value.ljust(collumn_size)  # if users entry is too short, pad with spaces  
                        
                    rows_array.append(value)

                # Append the record to file
                record_line = '|'.join(rows_array)
                with open(table_path, 'a') as f:
                    f.write('\n' + record_line)

                self._logger.info(f'Inserted record into {table_name}: {record_line.strip()}')

                more = input("More entries? (y/n): ").strip().lower()
                if more == 'n':
                    break

        except Exception as e:
            self._logger.fatal(f'Error while inserting into {table_name}: {e}')
