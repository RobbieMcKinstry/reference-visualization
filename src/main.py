import os

from flask import Flask
from flask import render_template
import bibtexparser

app = Flask(__name__)

BIBLIOGRAPHY_ROOT = 'bibliographies'
READ_ONLY_BIBS = {}

class BibEntry:

    def __init__(self, filename):
        # first, set the name entry
        self.name = filename.replace('.bib', '')
        # then, read in the file
        full_path = os.path.join(BIBLIOGRAPHY_ROOT, filename)
        self.href = 'localhost:5000/bib/{0}'.format(filename)

        with open(full_path) as bibtex_file:
            bib_database = bibtexparser.\
                bparser.\
                BibTexParser(common_strings=True).\
                parse_file(bibtex_file)

            self.entries = bib_database.entries

@app.route('/bib/<name>')
def bib(name=None):
    if name is None:
        return 'no such bibliography'
    bib = READ_ONLY_BIBS[name]
    return render_template('bib.html', bib=bib)

def populate_bibliographies():
    bibliographies = read_bibliography_list()
    return {f: BibEntry(f) for f in bibliographies }

@app.route('/')
def home():
    return render_template('index.html', bibliographies=READ_ONLY_BIBS)

def read_bibliography_list():
    files = os.listdir(BIBLIOGRAPHY_ROOT)
    bib_checker = lambda string: string.endswith('.bib')
    file_iterator = filter(bib_checker, files)
    return list(file_iterator)

READ_ONLY_BIBS = populate_bibliographies()
