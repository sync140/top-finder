import re
import os


def find_tops(fname):  # Erstellt Liste der TOPs aus einer .tex datei
    # Einlesen der Datei
    f = open(fname, 'r', encoding='utf-8')
    text = f.read()
    f.close()

    # Suchen von \TOP{Titel}, bzw. \Top{Titel} in dem Text und Extrahieren des Titels in eine Liste
    p = '\\\TOP\{(.+?)\}|\\\Top\{(.+?)\}'  # Pattern für RegEx. \TOP{...}, oder \Top{...}
    m = re.findall(p, text)  # Durchsucht Text nach jedem Auftreten des Patterns
    for i in range(len(m)):  # re speichert für jeden Fund ein Tupel einmal für \TOP und einmal für \Top
        if m[i][0] == '':
            m[i] = m[i][1]
        else:
            m[i] = m[i][0]
    return m  # Ausgegeben wird die Liste mit den Titeln aller TOPs


def find_date(fname):  # Gibt das Datum einer .tex Datei von einem Protokoll aus (Hätte man auch über den Dateinamen machen können)
    # Einlesen der Datei
    f = open(fname, 'r', encoding='utf-8')
    text = f.read()
    f.close()

    # Suchen nach \Tag{Datum} im Text und Extrahieren des Datums
    p = '\\\Tag\{(.+?)\}'  # Pattern für RegEx. \Tag{...}
    m = re.search(p, text)  # Sucht im Text nach dem Pattern
    if m:  # Wenn etwas gefunden wird
        return m.group(1)  # nur das Datum wiedergeben
    else:  # Nur falls eine Datei kein \Tag{} enthält... sollte aber unnötig sein.
        return 'Kein Datum'


def make_readme(dir):  # Erstellt eine Readme.md Datei mit einer Liste alle Protokolle und darin enthaltenen TOPs
    readme = open(dir + '/Readme.md', 'w', encoding='utf-8')  # Erstellen der Datei
    for file in os.listdir(dir):  # Geht alle Datein im Ordner durch
        if file.endswith('.tex'):  # Checkt ob sie .tex Dateien sind
            # print(file)  # Damit ich weiß bei welchen Dateien irgendwas kaputt geht
            path = dir + '/' + file  # Pfad einer Datei relativ zum working directory
            readme.write('Protokoll vom ' + find_date(path) + ':\n* ')  # Schreibt Protokoll vom *Datum*:
            readme.write('\n* '.join(find_tops(path)))  # Schreibt die Liste der TOPs. '* ' sorgt für Stichpunkte
            readme.write('\n\n')  # Leerzeile nach einem Protokoll
    readme.close()


#%% Auswerten von Mehreren Ordnern gleichzeitig
year = os.listdir('Protokolle')
year.pop()
year.pop()
for y in year:
    print(y)
    make_readme('Protokolle/' + y)
