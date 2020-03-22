#!/usr/bin/env python3

import sys
import pyexcel as pe

def get_country_code(country):
    if len(country) == 2:
        return country.lower()

	# In case more country codes need to be supported, this list might be
	# considered:
	# https://gist.github.com/walterrenner/1e72fad092b00ae7d998c703c0d41832
    country_codes = { 'Deutschland': 'de', 'Österreich': 'at', 'Schweiz': 'ch' }
    if country in country_codes:
        return country_codes[country]

    raise Exception('Unknown country "{}"'.format(country))

def extract_internal_data(generator):
    for row in generator:
        if row['Onlinekarte Intern'] == 'Ja':
            yield {'name': row['Vorname'] + ' ' + row['Name'], 'zip': row['PLZ'], 'country_code': get_country_code(row['Land']), 'style': 'mitglied'}

def extract_public_data(generator):
    for row in generator:
        if row['Onlinekarte Öffentlich'] == 'Ja':
            yield {'zip': row['PLZ'], 'country_code': get_country_code(row['Land']), 'name': 'Mitglied', 'style': 'mitglied'}

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
