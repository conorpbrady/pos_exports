import datetime
import csv
import subprocess
import os
import re

# These imports are imported into the PointOfSale factory method
#from lib.micros3700 import Micros3700
#from lib.simphony2 import Simphony2
#from lib.infogenesis import Infogenesis

class PointOfSale:

    @staticmethod
    def pos_class(pos_type, config):
        if pos_type.lower() == 'simphony2':
            from lib.simphony2 import Simphony2
            return Simphony2(config)
        elif pos_type.lower() == 'micros3700':
            from lib.micros3700 import Micros3700
            return micros3700.Micros3700(config)
        elif pos_type.lower() == 'infogenesis':
            from lib.infogenesis import Infogenesis
            return infogenesis.Infogenesis(config)

    def __init__(self):
        pass

    def set_run_date(self, run_date):
        self.business_date = run_date

    def load_query_from_file(self):
        with open(self.query_path, 'r') as file_handle:
            query_string = file_handle.read().replace('\r\n','')
        return query_string

    def gather_pos_data(self):
        pass

    def format_data(self):
        pass

    def clean_up(self):
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

    def format_as_currency(self, string):
        # This should be ran on all fields processed
        # If this is a currency field, format to 2 decimal places
        #  Should match: '4.0000','.0000','-3.2300004'
        #  Should not match: 'Tips','Hot and Sour Soup','3','Ch. Margaeux'
        #  RegEx: /(-?[0-9]*\.[0-9]+)/g
        
        pattern = re.compile('(-?[0-9]*\.[0-9]+)')
        return re.sub(pattern,
                      lambda match: '{0:.2f}'.format(float(match.group(0))),
                      string)
        

        
        

        

