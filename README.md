# LUKi Member Map

Dieses Projekt enthält Skripte zum Erstellen von KML-Dateien für Karten zur
Darstellung der Mitglieder von [LUKi - Linux User im Bereich der Kirchen e.V.](https://luki.org/)
Hierbei gibt es zwei Varianten:
* Öffentlich: Anzahl der Mitglieder an einem Ort wird angezeigt. Mitglieder mit
  `Ja` in der Spalte `Onlinekarte Öffentlich` werden berücksichtigt.
* Intern: Mit Vor- und Nachnamen. Mitglieder mit `Ja` in Spalte
  `Onlinekarte Intern` werden berücksichtigt.

Zum Einsatz kommen die beiden Skripte `extract-data.py` und `csv2kml.py`. Ersteres
extrahiert die nötigen Daten aus der ODS-Mitgliederliste und gibt sie als CSV
auf STDOUT aus. Dieses CSV dient als Eingabe für `csv2kml.py`, welches für die
PLZs Geo-Lookups durchführt und eine KML-Datei auf STDOUT ausgibt. Damit bei
erneuter Ausführung nicht die gleichen Geo-Lookups durchgeführt werden müssen,
werden die Koordinaten in der Datei `geolookup-cache.csv` im Arbeitsverzeichnis
gespeichert.

## Nutzung

Alle Abhängigkeiten sind im Pipfile eingetragen. Zur Installation der
Abhängigkeiten empfiehlt sich [pipenv](https://pipenv.readthedocs.io/).
```console
$ pipenv install
$ pipenv shell
```
Anschließend können die KML-Dateien wie folgt erstellt werden:
Öffentlich:
```console
$ ./extract-data.py --public Mitglieder.ods | ./csv2kml.py - >luki_public.kml
```
Intern:
```console
$ ./extract-data.py --internal Mitglieder.ods | ./csv2kml.py - >luki_internal.kml
```

`csv2kml.py` erwartet als Eingabe eine oder mehrere CSV-Dateien mit den Feldern
`zip`, `name`, und `style`. Weitere Felder werden ignoriert.
Für style kann `mitglied` oder `treffen` verwendet werden.
Wird für `name` der Wert `Mitglied` verwendet, erscheint bei mehrfachem Auftreten
an einem Ort nicht mehrfach `Mitglied`, sondern `n Mitglieder`, wobei n die Anzahl ist.

Als Datei kann `-` angegeben werden, um von STDIN zu lesen.
Sind beispielsweise die LUKi-Treffen in der Datei Treffen.csv und sollen mit
den Mitgliedern kombiniert werden, kann folgendes Kommando verwendet werden:
```console
$ ./extract-data.py --public Mitglieder.ods | ./csv2kml.py - Treffen.csv >luki_public.kml
```

Kommt es dabei zu einer Überschneidung (Mitglied und Treffen haben gleiche PLZ),
wird das Treffen leicht nach Südwesten verschoben (Höhen- und Breitengrad werden
um jeweils 0,01 verringert).

## Einschränkungen
Es wird davon ausgegangen, dass alle PLZs in Deutschland liegen.
