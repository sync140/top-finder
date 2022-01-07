import PyPDF2
import re
import os
#%%
def find_tops(fname):  # Erstellt eine Liste von TOPs aus einer .pdf datei
    with open(fname, 'rb') as f:
        doc = PyPDF2.PdfFileReader(f)  # Datei mit PyPDF2 einlesen

        TOP = []  # Leere liste an TOPs
        pattern = '^TOP\d+:$'  # RegEx pattern, der nach Strings sucht die mit TOP beginnen, dannach eine Zahl haben und mit einem ':' enden.
        for n in range(doc.numPages):  # loop über alle Seiten des Dokuments
            page = doc.getPage(n)
            text = page.extractText().splitlines()  # Extrahiert den Text der Seite in einen String und teil diesen an newlines auf in eine Liste
            for i in range(len(text)):  # loop über alle Einträge der Liste
                if re.fullmatch(pattern, text[i]):  # Sucht die Einträge TOP#: (# soll eine belibige Zahl sein)
                    TOP.append(text[i + 1])  # Der Eintag nach TOP#: ist dann der Titel des TOPs
                else:
                    pass
    return TOP  # Ausgeben der Liste


def find_date(fname):
    with open(fname, 'rb') as f:
        doc = PyPDF2.PdfFileReader(f)  # Datei mit PyPDF2 einlesen

        page = doc.getPage(0)  # page ist damit das Objekt der 1. Seite
        text = page.extractText().splitlines()  # Text der 1. Seite in einen String extrahieren und an den newlines in eine Liste aufteilen
        for i in range(len(text)):  # Loop über alle Enträge der Liste
            if text[i] == 'Sitzungsprotokoll':  # Bei dem Protokoll was ich als Beispiel genommen hab war das Datum direkt nach 'Sitzungsprotokoll'
                date = text[i+1]
                break
            else:
                date = 'Kein Datum'
    return date  # Datum ausgeben


def make_readme(dir):  # Erstellt eine Readme.md Datei mit einer Liste alle Protokolle und darin enthaltenen TOPs
    readme = open(dir + '/Readme.md', 'w', encoding='utf-8')  # Erstellen der Datei
    for file in os.listdir(dir):  # Geht alle Datein im Ordner durch
        if file.endswith('.pdf'):  # Checkt ob sie .pdf Dateien sind
            print(file)  # Damit ich weiß bei welchen Dateien irgendwas kaputt geht
            path = dir + '/' + file  # Pfad einer Datei relativ zum working directory
            readme.write('Protokoll vom ' + find_date(path) + ':\n* ')  # Schreibt Protokoll vom *Datum*:
            readme.write('\n* '.join(find_tops(path)))  # Schreibt die Liste der TOPs. '* ' sorgt für Stichpunkte
            readme.write('\n\n')  # Leerzeile nach einem Protokoll
    readme.close()

#%%
make_readme('Protokolle_PDF/2019')



