# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# License: MIT. See COPYING.MIT file in the Waldo distribution

from __future__ import division
import backend
from waldo.mgi.models import Entry
from waldo.translations.services import translate

def from_ensembl_gene_id(ensembl_gene_id, session=None):
    '''
    mgi_id = from_ensembl_gene_id(ensembl_gene_id, session={backend.create_session()})

    Convert ensembl_gene_id to mgi ID (MGI:00xxxxxx)

    Parameters
    ----------
      ensembl_gene_id : Ensembl gene ID
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      mgi_id : MGI ID
    '''
    return translate(ensembl_gene_id, 'ensembl:gene_id', 'mgi:id', session)

def retrieve_go_annotations(mgi_id, session=None):
    '''
    go_ids = retrieve_go_annotations(mgi_id, session={backend.create_session()})

    Retrieve GO ids by MGI ID.

    Parameters
    ----------
      mgi_id : mgi_id
      session : SQLAlchemy session to use (default: call backend.create_session())
    Returns
    -------
      go_ids : list of go terms (of the form "GO:00...")
    '''
    if session is None: session = backend.create_session()
    entr = session.query(Entry).filter(Entry.mgi_id == mgi_id).first()
    return [go.go_id for go in entr.annotations]