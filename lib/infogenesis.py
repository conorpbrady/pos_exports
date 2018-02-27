from lib.pointofsale import PointOfSale
from lib.infogenesisdatabase import InfogenesisDatabase


class Infogenesis(PointOfSale):
    

    def __init__():


    def init_database():
        ig_db = InfogenesisDatabase()
        ig_db.init_queries()
        ig_db.create_tables()
        ig_db.insert_values()
        
    def set_run_date():
        #configure filename to pull from zip
        pass

    def gather_pos_data():
        #Get Files from zip
        #Copy to temp folder
        #init database
        #Run query
        #load_results
        pass


    def format_data():
        pass


    def clean_up():
        for file in files:
            os.remove('temp\\{}'.format(file))
        #close db connection
        self.ig_db.close()
        #rem



    def get_files_from_zip(date_to_get, files_to_get, site_code, file_path):
        date_string = date_to_get.strftime('%Y%m%d')
        full_file_path = '{}{}_{}.zip'.format(file_path, site_code, date_string) 
        with zipfile.ZipFile(full_file_path, 'r') as zip_read:
            for file in files_to_get:
                zip_read.extract(file, path='temp\\')



        
                                            

                
                
