#!/usr/bin/env python3

import sys
import pyexcel as pe

def extract_internal_data(generator):
    for row in generator:
        if row['Onlinekarte Intern'] == 'Ja':
            yield {'name': row['Vorname'] + ' ' + row['Name'], 'zip': row['PLZ'], 'style': 'mitglied'}

def extract_public_data(generator):
    for row in generator:
        if row['Onlinekarte Öffentlich'] == 'Ja':
            yield {'zip': row['PLZ'], 'name': 'Mitglied', 'style': 'mitglied'}

def main(argv):
    if len(argv) != 3 or (argv[1] != '--public' and argv[1] != '--internal'):
        exit('Usage: {} --public|--internal <ods file>'.format(argv[0]))

    if argv[1] == '--public':
        public = True
    else:
        public = False
    odsFile = argv[2]

    records = pe.iget_records(file_name=odsFile)
    if public:
        io=pe.isave_as(records=extract_public_data(records), dest_file_type='csv', dest_lineterminator='\n')
    else:
        io=pe.isave_as(records=extract_internal_data(records), dest_file_type='csv', dest_lineterminator='\n')
    print(io.getvalue())

if __name__ == '__main__':
    main(sys.argv)
