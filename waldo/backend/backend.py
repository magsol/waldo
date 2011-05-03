# -*- coding: utf-8 -*-
# Copyright (C) 2009-2011, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import path
import logging

logging = logging.getLogger('backend')

_paths = [
    path.join(path.abspath(path.dirname(__file__)), '..', '..'),
    '.',
    '/var/lib/waldo',
    ]
database_file = 'waldo.sqlite3'
use_fts3 = True

for _basep in _paths:
    _fullp = path.join(_basep, 'waldo.sqlite3')
    if path.exists(_fullp):
        database_file = _fullp
        logging.info('Using database: %s' % database_file)
        break

Base = declarative_base()
engine = create_engine('sqlite:///' + database_file, echo=False)
metadata = Base.metadata
metadata.bind = engine
create_session = sessionmaker(bind=engine)

def create_tables():
    '''
    create_tables()

    Creates all tables in database.
    '''
    metadata.create_all()
    conn = engine.connect()
    if use_fts3:
        #drop the old uniprot organism entry, and create a virtual one with fts3
        conn.execute("drop table uniprot_entry")
        conn.execute("""CREATE VIRTUAL TABLE uniprot_entry USING fts3 (
                VARCHAR(32) NOT NULL,
                rname VARCHAR(128) NOT NULL,
                sequence TEXT,
                PRIMARY KEY (name))""")


