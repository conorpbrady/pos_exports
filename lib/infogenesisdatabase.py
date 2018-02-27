import sqlite3
import csv

class InfogenesisDatabase():
    def __init__(self, db_filename):
        self.connection = sqlite3.connect(db_filename)
        self.table_create_queries = []
        self.column_headers = {}
        self.data_insert_values = {}
        self.tables = []

    def run_query(self, query):
        cur = self.connection.cursor()
        cur.execute(query)

        # cur.fetchall returns tuples - convert to list then return
        return [list(r) for r in cur.fetchall()]
        
    def create_tables(self):
        for query in self.table_create_queries:
            cur = self.connection.cursor()
            cur.execute(query)
   

    def insert_values(self):  
        for table in self.tables:
            cur = self.connection.cursor()
            blank_values = ['?'] * len(self.data_insert_values[table][0])      
            query = "INSERT INTO {} ({}) VALUES({})".format(table, ','.join(self.column_headers[table]),','.join(blank_values))
            cur.executemany(query, self.data_insert_values[table])
            self.connection.commit()
                
    def init_queries(self):
        self.definition_table_queries(['data\\infogenesis\\omnia_tenders.csv','data\\infogenesis\\omnia_discounts.csv'])
        self.data_table_queries()

    def definition_table_queries(self,filenames):
        for file in filenames:
            with open(file,'r') as r:
                csv_reader = csv.reader(r, quotechar='"')
                for row in csv_reader:
                    table = row[1]
                    break
                self.table_create_queries.append("CREATE TABLE IF NOT EXISTS {} (ID, Name);".format(table))
                self.column_headers[table] = ['ID', 'Name']
                self.tables.append(table)
                path = ''
                self.data_insert_values[table] = self.get_data_values(path, file, table, [['1','ID'],['2','Name']], True)

    def data_table_queries(self):
        with open('data\\infogenesis\\db_build.csv','r') as r:
            csv_reader = csv.reader(r, quotechar='"')
            tables = {}
            next(csv_reader,None) # Skip Headers

            for row in csv_reader:

                values_list = [row[1],row[2],row[3]]
                if row[0] not in tables:
                    tables[row[0]] = [values_list]
                else:
                    tables[row[0]].append(values_list)
            
            for filename, all_fields in tables.items():
                table_name = filename[:filename.find('.')]
                self.tables.append(table_name)
                
                self.column_headers[table_name] = [item[1] for item in all_fields]

                query = ('CREATE TABLE IF NOT EXISTS {} (Unique_ID INTEGER NOT NULL PRIMARY KEY, {})'
                         .format(table_name,
                                 ', '.join(map(lambda s: ' '.join(s[1:]),all_fields))))

                self.data_insert_values[table_name] = self.get_data_values('temp\\', filename, table_name, all_fields, False)
                self.table_create_queries.append(query)

                
    def get_data_values(self, path, filename, table, all_fields, skip_headers):
        data_values = []
        row_numbers = []
        for fields in all_fields:
            row_numbers.append(fields[0])
            
        with open(path + filename,'r') as r:
            quoted_list = [line.replace('{','|').replace('}','|') for line in list(r)]
            
            csv_reader = csv.reader(quoted_list, quotechar='|')
            if skip_headers: next(csv_reader, None)
            for row in csv_reader:
                values = []
                for row_number in row_numbers:
                    values.append(row[int(row_number)-1].strip('$').strip('"'))
                data_values.append(tuple(values))
        return data_values

    def close(self):
        self.connection.close()




    
