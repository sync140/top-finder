import os
import sys
import re
import fitz


def find_tops(filename):
    """Erstellt eine Liste von TOPs aus einer PDF- oder HTML-Datei."""
    tops = []
    
    if filename.endswith('.pdf'):
        with fitz.open(filename) as doc:
            pattern = re.compile(r'^TOP \d+:? (.*)$', re.MULTILINE)

            for page in doc:
                matches = pattern.findall(page.get_text())
                tops.extend(matches)
    elif filename.endswith('.html'):
        with open(filename) as f:
            text = f.read()
            pattern = re.compile(r'^<H2>\d+\. (.*):</H2>$', re.MULTILINE)
            tops = pattern.findall(text)

    return tops


def make_readme(dir):
    """
    Erstellt eine README.md Datei mit einer Liste alle Protokolle und darin
    enthaltenen TOPs.
    """
    with open(os.path.join(dir, 'README.md'), 'w+', encoding='utf-8') as readme:
        # Zähle wie viele Protokolle und TOPs ausgelesen wurden
        num_files = 0
        num_tops = 0

        for file in os.listdir(dir):
            # Lese nur PDF- und HTML-Dateien ein
            if not (file.endswith('.pdf') or file.endswith('.html')):
                continue

            path = os.path.join(dir, file)

            # Wenn der Dateiname nicht geändert wurde, hat er das Format FS-Protokoll_YYYY-MM-DD_public.pdf/html
            date = f'{file[21:23]}.{file[18:20]}.{file[13:17]}'
            tops = find_tops(path)

            if len(tops) == 0:
                readme.write(f'Keine TOPS im Protokoll vom {date} gefunden.')
            else:
                # Schreibe die TOPs in Stichpunkten
                readme.write(f'Protokoll vom {date}:\n* ')
                readme.write('\n* '.join(tops))
                readme.write('\n\n')

            num_files += 1
            num_tops += len(tops)

    print(f'Es wurden insgesamt {num_files} Protokolle eingelesen und {num_tops} TOPs gefunden.')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Kein Ordner gegeben.')
        sys.exit()

    dir = sys.argv[1]
    if not os.path.isdir(dir):
        print(f'"{dir}" ist kein Ordner.')
        sys.exit()

    make_readme(dir)

