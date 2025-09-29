import Table

class DBFile:
    def __init__(self,argTables:list):
        self.tables = argTables
        self.__sizeof__ = len(argTables)

    def __str__(self):
        return 'Class for working with tables in the EQ_Database system.'
    
    def createTable(self):
        name = input('Enter table name: ')
        print('You will be prompted to insert collumns, to quit type q')
        
        table = Table(argCollumns=[])
        
        do:
            table.
