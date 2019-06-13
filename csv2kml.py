#!/usr/bin/env python3

import os
import sys
import csv
from geopy.geocoders import Nominatim

CACHEFILE = 'geolookup-cache.csv'

cache = {}
placemarks_by_style = {}
valid_styles = ['mitglied', 'treffen']
geolocator = Nominatim(user_agent='python')

def load_lookup_cache():
    if not os.path.isfile(CACHEFILE):
        return

    with open(CACHEFILE, newline='') as cachefile:
        reader = csv.DictReader(cachefile)
        for row in reader:
            cache[row['zip']] = row

def store_lookup_cache():
    with open(CACHEFILE, 'w', newline='') as cachefile:
        fieldnames = ['zip', 'lat', 'lon']
        writer = csv.DictWriter(cachefile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cache.values())

def lookup(zip):
    if not zip in cache:
        location = geolocator.geocode(zip + ', Germany')
        cache[zip] = {'zip': zip, 'lat': location.latitude, 'lon': location.longitude}

    return cache[zip]

def print_kml(placemarks_by_style):
    print('''\
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>LUKi e.V. - Mitglieder und Treffen</name>
    <Style id="mitglied">
        <IconStyle>
        <Icon>
            <href>../../../../wp-content/uploads/2018/11/user.png</href>
        </Icon>
        </IconStyle>
    </Style>
    <Style id="treffen">
        <IconStyle>
        <Icon>
            <href>../../../../wp-content/uploads/2018/11/home.png</href>
        </Icon>
        </IconStyle>
    </Style>''')

    used_coords = {}
    for style, placemarks in placemarks_by_style.items():
        for coord_key in sorted(placemarks.keys()):
            placemark = placemarks[coord_key]
            while coord_key in used_coords:
                # coordinate already used with a different style; move slightly
                placemark['lon'] = float(placemark['lon']) - 0.01
                placemark['lat'] = float(placemark['lat']) - 0.01
                coord_key = '{}_{}'.format(placemark['lon'], placemark['lat'])
            used_coords[coord_key] = True
            names = sorted(placemark['names'])
            mitgliedCount = names.count('Mitglied')
            if mitgliedCount > 1:
                names[:] = (name for name in names if name != 'Mitglied')
                names.append('{} Mitglieder'.format(mitgliedCount))

            name = '<br>'.join(names)
            print('''\
    <Placemark>
        <name><![CDATA[{}]]></name>
        <styleUrl>#{}</styleUrl>
        <Point>
        <coordinates>{}, {}</coordinates>
        </Point>
    </Placemark>'''.format(name, style, placemark['lon'], placemark['lat']))

    print('</Document>\n</kml>')

def read_placemarks(file):
    if file == '-':
        csvfile = sys.stdin
    else:
        csvfile = open(file)

    with csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not row['style'] in valid_styles:
                print(row)
                exit('Invalid style "{}"'.format(row))

            if not row['style'] in placemarks_by_style:
                placemarks_by_style[row['style']] = {}
            coord = lookup(row['zip'])
            coord_key = '{}_{}'.format(coord['lon'], coord['lat'])
            if not coord_key in placemarks_by_style[row['style']]:
                placemarks_by_style[row['style']][coord_key] = {'names': []}
                placemarks_by_style[row['style']][coord_key].update(coord)
            placemarks_by_style[row['style']][coord_key]['names'].append(row['name'])

def main(argv):
    if len(argv) == 1 or argv[1] == '-h' or argv[1] == '--help':
        exit('Usage: {} <csv file> [...]\nUse - to read from STDIN.'.format(argv[0]))

    load_lookup_cache()
    for file in argv[1:]:
        read_placemarks(file)
    store_lookup_cache()

    print_kml(placemarks_by_style)

if __name__ == '__main__':
    main(sys.argv)
