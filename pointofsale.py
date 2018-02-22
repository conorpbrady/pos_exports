import datetime
import csv
import subprocess
import os

class PointOfSale:

    @staticmethod
    def pos_class(pos_type, config):
        if pos_type.lower() == 'simphony2':
            return Simphony2(config)
        elif pos_type.lower() == 'micros3700':
            return Micros3700(config)
        elif pos_type.lower() == 'infogenesis':
            return Infogenesis(config)


    def __init__(self):
        pass

    def set_run_date(self, run_date):
        self.business_date = run_date

    def load_query_from_file(self):
        with open(self.query_path, 'r') as file_handle:
            query_string = file_handle.read().replace('\r\n','')
        return query_string

    def gather_pos_data():
        pass

    def format_pos_data():
        pass

    def write_file(self, filename):
        with open(filename, 'w') as w:
            file_writer = csv.writer(w)
            for row in self.results:
                file_writer.writerow(row)
    
    def as_float(string):
        return float(string.strip('$'))

    def get_today():
        return datetime.date.today()

    def get_yesterday():
        return datetime.date.fromordinal(datetime.date.today().toordinal()-1)


class Micros3700(PointOfSale):

    def __init__(self, config):
        
        self.db_user = config['User']
        self.db_pass = config['Password']
        self.db_name = config['Database']
        self.query_path = config['QueryFilePath']
        self.results = []
        self.sql_query = ''
        self.temp_file_path = 'temp_output.txt'
        
    def load_query_from_file(self):
        query_string = super().load_query_from_file()        

        footer = "; OUTPUT TO {} DELIMITED by ','".format(self.temp_file_path)
        self.sql_query = query_string + footer
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
        #print(' '.join(map(lambda s: s.replace('\n',' '), cmd)))

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = p.communicate()

        
    def load_query_results(self):
        with open(self.temp_file_path,'r') as r:
            csv_reader = csv.reader(r, quotechar="'")
            for row in csv_reader:
                self.results.append(row)
        os.remove(self.temp_file_path)

    def gather_pos_data(self):
        self.load_query_from_file()
        self.run_query()
        self.load_query_results()

    def format_data(self):
        pass

    def clean_up(self):
        pass
    
    #def write_file(self, filename):
    #    with open(filename, 'w') as w:
    #        file_writer = csv.writer(w)
    #        for row in self.results:
    #            file_writer.writerow(row)
        

    #def as_float(string):
    #    return '{:.2f}'.format(string.strip('$'))



class Simphony2(PointOfSale):

    def __init__(self, config, date_to_run):
        self.db_user = config['User']
        self.db_pass = config['Password']
        self.results = []
        self.sql_query = ''
        self.start_date = date_to_run
        self.end_date = datetime.date.fromordinal(date_to_run.toordinal()-1)
        


    def gather_pos_data():
        sql_query = "DECLARE @yDay datetime;DECLARE @tDay datetime;" \
                "SET @yDay='" + self.start_date.isoformat() + " 04:00:00';" \
                "SET @tDay='" + self.end_date.isoformat() + " 04:00:00';"
        sql_query += super().load_sql_query_from_file('sqlQuery.txt');

        cmd = [
            "sqlcmd",
            "-S",".\sqlexpress",
            "-U",self.db_user,
            "-P",self.db_pass,
            "-d","CheckPostingDB",
            "-Q",sql_query,
            "-s",",",
            "-h","-1",
            "-w","700",
            "-W"
            ]

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = p.communicate()
        sales_list = out.decode(encoding='UTF-8').split('\r\n')
    
        results = sales_list[:-3]

class Infogenesis(PointOfSale):
    pass
