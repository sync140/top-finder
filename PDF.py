import os
import sys
import re
import fitz


def find_tops(filename):
    """Erstellt eine Liste von TOPs aus einer PDF- oder HTML-Datei."""
    text = ""

    if filename.endswith('.pdf'):
        pattern = re.compile(r'^TOP \d+:? (.*)$', re.MULTILINE)
        with fitz.open(filename) as doc:
            for page in doc:
                text += page.get_text()
    elif filename.endswith('.html'):
        # TODO regex richtig schreiben
        pattern = re.compile(r'^<[Hh]2>(?:\d+\. )?(.*):?</[Hh]2>$', re.MULTILINE)
        with open(filename) as f:
            text = f.read()

    return pattern.findall(text)


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
                readme.write(f'Keine TOPS im Protokoll vom {date} gefunden.  \n')
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

