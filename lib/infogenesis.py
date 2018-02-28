from lib.pointofsale import PointOfSale
from lib.infogenesisdatabase import InfogenesisDatabase
import zipfile
import csv
import os

class Infogenesis(PointOfSale):
    

    def __init__(self, config):

        self.file_path = config['SalesFilePath']
        self.db_definition = config['DatabaseDefinitionFile']
        self.ig_db = InfogenesisDatabase('temp\\temp.db')
        self.site_code = config['SiteCode']
        
        super().__init__(config)

    def create_database(self):

        self.ig_db.init_queries()
        self.ig_db.create_tables()
        self.ig_db.insert_values()
        
    def gather_pos_data(self):

        self.get_files_from_zip()
        self.create_database()
        self.results = self.ig_db.run_query(super().load_query_from_file())

    def clean_up(self):    

        self.ig_db.close()
        for file in os.listdir('temp\\'):
            os.remove('temp\\{}'.format(file))


    def get_files_from_zip(self):
        date_string = self.business_date.strftime('%Y%m%d')
        full_file_path = '{}{}\\{}_{}.zip'.format(self.file_path,
                                                  self.site_code,
                                                  self.site_code,
                                                  date_string)
        
        with zipfile.ZipFile(full_file_path, 'r') as zip_read:
            for file in self.files_needed():
                zip_read.extract(file, path='temp\\')


    def files_needed(self):
        files = []
        with open(self.db_definition,'r') as r:
            csv_reader = csv.reader(r)
            for row in csv_reader:
                if row[0] not in files:
                    files.append(row[0])

        return files[1:] #Skips Header
        
                                            

                
                
