from lib.pointofsale import PointOfSale
from lib.connection import Connection
import argparse
import configparser
import datetime
import os


def main():
    parser = argparse.ArgumentParser(description='Generic script to export ' \
                                     'from POS database or stored pos files.' \
                                     ' See README.md or docs/ for details.')
    parser.add_argument('-d','--date',metavar='date',
                        help='Date to run as mm-dd-yyy')

    args = parser.parse_args()

    if args.date:
        run_date = datetime.datetime.strptime(args.date, '%m-%d-%Y').date()
    else:
        run_date = datetime.date.fromordinal(
        datetime.date.today().toordinal()-1)

    config = configparser.ConfigParser()
    config.read('settings\\settings.ini')
    
    output_filename = '{}{}.{}'.format(config['General']['OutputFileName'],
                                   run_date.strftime('%Y%m%d'),
                                   config['General']['OutputFileExtension'])


    pos_type = config['General']['POS']

           
    pos = PointOfSale.pos_class(pos_type, config[pos_type])

    pos.set_run_date(run_date)
    pos.gather_pos_data()
    pos.format_data()
    pos.write_file(output_filename)
    pos.clean_up()


    connection_type = config['General']['Connection']
    conn_handler = Connection.connection_class(connection_type,
                                           config[connection_type])
    conn_handler.connect()
    conn_handler.change_remote_directory(config[connection_type]['RemotePath'])
    conn_handler.upload_file(output_filename)
    conn_handler.close()


    os.replace(output_filename,
          config['General']['ArchiveFolder'] + output_filename)


if __name__ == '__main__':
    main()
