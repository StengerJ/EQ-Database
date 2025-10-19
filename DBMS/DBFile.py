import os
import logging
import re
class DBFile:
    def __init__(self,argDBFilePath='Tables/dbFiles.db'):
        self._path = argDBFilePath

        if not os.path.exists(self._path):
            try:
                with open(self._path,'x') as f:
                    f.write('FILE_NAME COLUMN_NAME COLUMN_SIZE \n')
                    print(f'Main table was not created, created it at this path: {self._path}')
            except Exception as e:
                print(f'Error creating dbFiles.db: {e}')
            

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

        if os.path.exists(f'Tables/{table_name.upper()}.db'):
            print('Table already exists, please choose another name or insert into that table.')
            return
        print('You will be prompted to insert collumns')
        print('When you are finished entering collumns type anything but an number in a the length of your next collumn.')
        
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
                        break
                    else:
                        f.write(f'{table_name}|{collumn_name}|{length} \n')
                        collumns.append((collumn_name,length))
            
            """
            Make the individual table file, open it in append mode. This also creates the table if it does not exist.
            """
            with open(f'Tables/{table_name}.db','a') as t:
                table_str = ''
                for tup in collumns:
                    x,y = tup
                    if len(table_str) == 0:
                        table_str += f'{x}({y})'
                    else:
                        table_str += ' ' + f'{x}({y})'
                
                t.write(table_str)
        except Exception as e:
            print(f'Error creating table {e}')
    def insert(self):
        """
        Function that allows a user to insert data into an existing table.
        These events happen:
        1. The user is prompted to enter the table name they wish to insert into.
        2. The program checks to see if the table exists, if not it returns.
        3. The program reads the collumn definitions from the table file.
        4. The user is prompted to enter data for each collumn, with truncation or padding as needed.
        5. The data is appended to the table file.
        6. The user is asked if they wish to insert more data, if not the function returns.
        7. Appropriate logging is done throughout the process.
        """
        table_name = input('Enter Table Name: ').upper()
        table_path = f'Tables/{table_name}.db'

        if not os.path.exists(table_path):
            print('Table does not exist, please create it first.')
            return

        try:
            with open(table_path, 'r') as f:
                header = f.readline().strip()
                if not header:
                    print("Table has no defined columns.")
                    return

            columns = []
            for col_def in header.split(' '):
                match = re.match(r'(\w+)\((\d+)\)', col_def)
                if match:
                    collumn_name, collumn_size = match.groups()
                    columns.append((collumn_name, int(collumn_size)))

            if not columns:
                print("No valid columns found in header.")
                return

            while True:
                rows_array = []
                for collumn_name, collumn_size in columns:
                    value = input(f"{collumn_name}: ").strip()
                    if len(value) > collumn_size:
                        value = value[:collumn_size]
                    if len(value) < collumn_size:
                        value = value.ljust(collumn_size)
                        
                    rows_array.append(value)

                record_line = '|'.join(rows_array)
                with open(table_path, 'a') as f:
                    f.write('\n' + record_line)

                more = input("Insert more entries? (y/n): ").strip().lower()
                if more == 'n':
                    break

        except Exception as e:
            print(f'Error while inserting into {table_name}: {e}')
    
    def delete(self):
        """
        Function that allows the user to delete a row from the database.
        Steps:
        1. Prompt for table name.
        2. Check if table exists.
        3. Read column definitions (header).
        4. Ask user for a search term to identify which row to delete.
        5. Locate the line and mark the first character with a tombstone (#).
        6. Continue if user wants to delete more.
        """
        table_name = input('Enter Table Name: ').upper()
        table_path = f'Tables/{table_name}.db'

        if not os.path.exists(table_path):
            print('Table does not exist, please create it first.')
            return

        try:
            with open(table_path, 'r') as f:
                header = f.readline().strip()
                if not header:
                    print("Table has no defined columns.")
                    return

            while True:
                row_to_delete = input("Enter a value from the row you want to delete: ").strip()
                is_row_deleted = False

                with open(table_path, 'r+') as f:
                    lines = f.readlines()
                    f.seek(0)

                    pos = 0
                    for line in lines:
                        line_length = len(line)
                        if line.startswith("#") or not line.strip():
                            pos += line_length
                            continue

                        if row_to_delete in line:
                            f.seek(pos)
                            f.write('#')
                            print(f"Record marked as deleted: {line.strip()}")
                            is_row_deleted = True
                            break
                        pos += line_length

                if not is_row_deleted:
                    print("No matching row found.")

                more = input("Delete more entries? (y/n): ").strip().lower()
                if more == 'n':
                    break

        except Exception as e:
            print(f'Error while deleting from {table_name}: {e}')
    
    def printFile(self):
        """
        Function that prints the contents of a table file.
        1. Prompts user for table name.
        2. Checks if table exists.
        3. Prints headers and data (skipping deleted rows).
        """
        inp = input('Enter a Table you wish to print: ').upper()
        table_path = f'./Tables/{inp}.db'

        if not os.path.exists(table_path):
            print('Error printing table, table does not exist. Please create it first.')
            return

        try:
            with open(table_path, 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]

            if not lines:
                print("Table is empty.")
                return

            collumns = lines[0]
            print("\n" + "-" * 100)
            print(f"TABLE: {inp}")
            print("-" * 100)
            print('Collumns: '+ collumns)
            print("-" * 100)

            for line in lines[1:]:
                if not line.startswith('#'):
                    print(line)

            print("-" * 100)
        except Exception as e:
            print(f'Error while attempting to print table for user: {e}')

    def purge(self):
        """
        Function that permanently removes deleted ('#') rows
        from all tables listed in dbFiles.db. Trys the following events in order:
        1. if the path to the main table/ metadata table dne return else continue through function
        2. open the tables file in read mode and get all the lines
        3. make a set of tables so we know there are no duplicates
        4. for each line in the metadata file(dbFiles.db, excluding the header/collumn names)
             get the table name and then add it to a list of table names without whitepace and other items.
        5. if no tables are in the file, then return / the set it empty return
        6. for each table in the set if the tables file exists then open the file read all the lines that do not start with a tombstone then write over the file
        7. after this function is called in the main.py the program will exit/return.
        """
        try:
            if not os.path.exists('./Tables/dbFiles.db'):
                return

            with open('./Tables/dbFiles.db', 'r') as f:
                lines = f.readlines()

            tables = set()
            for line in lines[1:]:
                table_name = line.strip().split('|')
                if len(table_name) >= 1 and table_name[0]:
                    tables.add(table_name[0].strip())

            if not tables:
                return

            for table in tables:
                table_path = f'./Tables/{table}.db'
                if not os.path.exists(table_path):
                    continue
                
                with open(table_path, 'r') as f:
                    lines = f.readlines()

                non_tomstone_lines = [line for line in lines if not line.startswith('#')]

                with open(table_path,'w') as f:
                    f.writelines(non_tomstone_lines)

        except Exception as e:
            print(f'Error purging: {e}')