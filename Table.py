class Table:
    
    def __init__(self,argCollumns:list):
        self._collumns = argCollumns

    def __str__(self):
        return 'Table class for a specific database table'
    
    def print_collumns(self):
        for col in self._collumns:
            print(col ,' ', col[col])