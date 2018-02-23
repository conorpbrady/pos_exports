import datetime
import subprocess
import os
from lib.pointofsale import PointOfSale

class Simphony2(PointOfSale):

    def __init__(self, config):
        self.db_user = config['User']
        self.db_pass = config['Password']
        self.results = []
        self.sql_query = ''
        self.query_path = config['QueryFilePath']

    def set_run_date(self, date_to_run):
        self.start_date = date_to_run
        self.end_date = datetime.date.fromordinal(date_to_run.toordinal()+1)
        


    def gather_pos_data(self):
        sql_query = "DECLARE @startDate datetime;DECLARE @endDate datetime;" \
                "SET @startDate='" + self.start_date.isoformat() + " 04:00:00';" \
                "SET @endDate='" + self.end_date.isoformat() + " 04:00:00';"
        sql_query += super().load_query_from_file()

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

        self.results = sales_list[:-3]

    def format_data(self):
        temp = []
        for row in self.results:
            temp.append(row.split(','))
        self.results = temp
