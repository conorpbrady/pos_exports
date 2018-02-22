from micros3700 import Micros3700
import connection
import argparse
import configparser
import datetime
import os

parser = argparse.ArgumentParser(description='Generic script to export ' \
                                      'from micros database.')
parser.add_argument('-d','--date',metavar='date',
                        help='Date to run as mm-dd-yyy')

config = configparser.ConfigParser()
config.read('settings.ini')

args = parser.parse_args()

if args.date:
    run_date = datetime.datetime.strptime(args.date, "%m-%d-%Y").date()
else:
    run_date = datetime.date.fromordinal(
    datetime.date.today().toordinal()-1)
    
output_filename = '{}{}.{}'.format(config['General']['OutputFileName'],
                                   run_date.strftime('%Y%m%d'),
                                   config['General']['OutputFileExtension'])

m = Micros3700(config['Micros3700'], run_date)

m.load_query_from_file('sql_query.txt')
m.run_query()
m.load_query_results()
m.write_file(output_filename)



connection_type = config['General']['Connection']
is_ftp_connection = (connection_type.lower() == 'sftp' or
                     connection_type.lower() == 'ftp')

conn_handler = Connection.connnection_class(connection_type,
                                           config[connection_type])

conn_handler.connect()
if is_ftp_connection:
    conn_handler.change_remote_directory(config[connection_type]['RemotePath'])
conn_handler.upload_file(output_filename)
conn_handler.close()


os.rename(output_filename,
          config['General']['ArchiveFolder'] + output_filename)


