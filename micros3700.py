import subprocess
import csv
import os

class Micros3700:

    def __init__(self, config, date_to_run):
        self.business_date = date_to_run
        self.db_user = config['User']
        self.db_pass = config['Password']
        self.db_name = config['Database']
        self.results = []
        self.sql_query = ''
        self.temp_file_path = 'temp_output.txt'
        
    def load_query_from_file(self, filename):
        with open(filename, 'r') as file_handle:
            query_string = file_handle.read().replace('\r\n','')

        footer = "; OUTPUT TO {} DELIMITED by ','".format(self.temp_file_path)
        self.sql_query = query_string+ footer
        self.replace_sql_variable('@businessDate', self.business_date)
            
    def replace_sql_variable(self, string, d):
        self.sql_query = self.sql_query.replace(string,"'{} 00:00:00'".format(d.isoformat()))

    def run_query(self):
        cmd = [
            "dbisql",
            "-c",
            "uid=" + self.db_user + ";pwd=" + self.db_pass,
            "-d",";",
            "-datasource",
            self.db_name,
            self.sql_query
            ]
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = p.communicate()
        #sales_list = out.decode(encoding='UTF-8').split('\r\n')
        
    def load_query_results(self):
        with open(self.temp_file_path,'r') as r:
            csv_reader = csv.reader(r, quotechar="'")
            for row in csv_reader:
                self.results.append(row)
        os.remove(self.temp_file_path)
                
    
    def write_file(self, filename):
        with open(filename, 'w') as w:
            file_writer = csv.writer(w)
            for row in self.results:
                file_writer.writerow(row)
        

    def as_float(string):
        return '{:.2f}'.format(string.strip('$'))

