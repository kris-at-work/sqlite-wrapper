import sqlite3
from sqlite3 import Error
import json

class SQLite:
    
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.table = None
        self.columns = None
        
    def check_table(self):
        table_data = {
            'name': self.table,
            'columns': self.columns
        }
        if self.table == None:
            print('Select table first')
        return table_data if self.table != None else False
        
    def where_delimiter(self,key):
        key = str(key).split('__')
        return f'{key[0]} {key[1] if len(key) == 2 else "="}'
    
    def where_str(self,where):
        return "WHERE " + " AND ".join(map(lambda x: f'{self.where_delimiter(x)} "{where[x]}"', where.keys()))
    
    
    def connect(self, db_name):
        try:
             self.conn = sqlite3.connect(db_name)
             self.cursor = self.conn.cursor()
        except Error as e:
            print(e)
        
    def set_table(self, table):
        if self.conn:
            try:
                self.table = table
                self.cursor.execute(f'PRAGMA table_info("{table}")')
                self.columns = [i[1] for i in self.cursor.fetchall()]
                return self.columns
            except Error as e:
                print(e)
        else:
            print('No connection. Connect DB first.')
        
    def close(self):
        try:
            self.conn.close()
        except Error as e:
            print(e)
        
    def push(self, data):
        if self.check_table() is False:
            return
        keys = list(data.keys())
        values = list(data.values())
        query_str = f'INSERT INTO {self.table} ({",".join(map(str,keys))}) VALUES ({",".join(map(lambda x: "?",keys))})'
        try:
            self.cursor.execute(query_str,values)
            self.conn.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(e)
    
    def push_array(self, data):
        if self.check_table() is False:
            return
        keys = list(data[0].keys())
        values = list(map(lambda el: list(el.values()),data))
        query_str = f'INSERT INTO {self.table} ({",".join(map(str,keys))}) VALUES ({",".join(map(lambda x: "?",keys))})'
        try:
            self.cursor.executemany(query_str,values)
            self.conn.commit()
            return self.cursor.rowcount
        except Error as e:
            print(e)
            
    def update(self,where = '',data = ''):
        if self.check_table() is False:
            return
        if where == '' or data == '':
            print('"where" and "data" is needed')
        if where != '':
            where = where if type(where) is str else self.where_str(where)
        keys = list(data.keys())
        values = list(data.values())
        query_str = f'UPDATE {self.table} SET {",".join(map(lambda x: f"{x} = ?",keys))} ' + where
        try:
            self.cursor.execute(query_str,values)
            self.conn.commit()
            return self.conn.total_changes
        except Error as e:
            print(e)
 
    def delete(self, where = ''):
        if self.check_table() is False:
            return
        if where == '':
            print('"where" is needed')
        if where != '':
            where = where if type(where) is str else self.where_str(where)
        query_str = f'DELETE FROM {self.table} ' + where
        try:
            self.cursor.execute(query_str)
            self.conn.commit()
            return self.conn.total_changes
        except Error as e:
            print(e)
    
    def get(self,where = ''):
        if self.check_table() is False:
            return
        if where != '':
            where = where if type(where) is str else self.where_str(where)
        col_string = ",".join(map(lambda x: f"'{x}', {x}", self.columns))
        query_str = f'SELECT json_group_array(json_object({col_string})) FROM {self.table} ' + where
        try:
            res = self.cursor.execute(query_str).fetchone()
            return json.loads(res[0]) if len(res) > 0 else []
        except Error as e:
            print(e)
            
    def exist(self,where = ''):
        res = self.get(where)
        return False if res == [] else res
            
    def create_table(self,data):
        table = data['name']
        columns_query = data['query']
        query_str = f'CREATE TABLE {table}({columns_query})'
        try:
            self.cursor.execute(query_str)
        except Error as e:
            print(e)
            
    def drop_table(self):
        if self.check_table() is False:
            return
        query_str = f'DROP TABLE {self.table}'
        try:
            self.cursor.execute(query_str)
            self.table = None
            self.columns = None
        except Error as e:
            print(e)
    
    def query(self,query_str: str, fetch_param = None, data = None):
        try:
            if data == None:
                if fetch_param == 'all':
                    return self.cursor.execute(query_str).fetchall()
                elif fetch_param == 'many':
                    return self.cursor.execute(query_str).fetchmany()
                elif fetch_param == 'one':
                    return self.cursor.execute(query_str).fetchone()
                else:
                    return self.cursor.execute(query_str)
            else:
                self.cursor.execute(query_str, data)
                self.conn.commit()
        except Error as e:
            print(e)
        except TypeError as t_e:
            print(t_e)