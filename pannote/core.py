# pannote --- search your txt documents
# Copyright (C) 2015-present  Honza Pokorny

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from shutil import rmtree

import xapian
import click


def out(s, line_ending='\n'):
    sys.stdout.write(s + line_ending)


def init(db_path):
    database = xapian.WritableDatabase(db_path, xapian.DB_CREATE_OR_OPEN)

    indexer = xapian.TermGenerator()
    stemmer = xapian.Stem("english")
    indexer.set_stemmer(stemmer)

    return database, indexer, stemmer


def index(db, indexer, filename):
    doc = xapian.Document()
    doc.add_value(0, os.path.basename(filename))

    with open(filename) as f:
        data = f.read()

    doc.set_data(data)

    indexer.set_document(doc)
    indexer.index_text(data)

    db.add_document(doc)


def index_directory(db, indexer, directory):
    files = os.listdir(directory)

    for f in files:
        full = os.path.join(directory, f)
        index(db, indexer, full)


def search(db, indexer, stemmer, term):
    enquire = xapian.Enquire(db)
    qp = xapian.QueryParser()
    qp.set_stemmer(stemmer)
    qp.set_database(db)
    qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
    query = qp.parse_query(term)
    enquire.set_query(query)
    matches = enquire.get_mset(0, 100)

    for m in matches:
        for v in m.document.values():
            if v.num == 0:
                yield v.value


@click.command()
@click.argument('directory', nargs=1)
@click.argument('term', nargs=1)
@click.option('-0', '--print0', is_flag=True, default=False,
              help='separate matches with a null byte in output')
def main(directory, term, print0):
    """
    A simple program that indexes a directory of text files and allows
    you to search it
    """
    db, indexer, stemmer = init('db')
    index_directory(db, indexer, directory)
    results = search(db, indexer, stemmer, term)

    for r in results:
        path = os.path.join(directory, r)
        out(path, '\0' if print0 else '\n')

    rmtree('db')
