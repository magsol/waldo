# -*- coding: utf-8 -*-
# Copyright (C) 2009, Luís Pedro Coelho <lpc@cmu.edu>
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

from __future__ import division
import networkx as nx
from collections import namedtuple
import os
_basedir = os.path.dirname(os.path.abspath(__file__))
G = nx.DiGraph()
Term = namedtuple('Term', 'id name is_a is_obsolete')
id = None
terms = []
for line in file(_basedir + '/gene_ontology.1_2.obo'):
    line = line.strip()
    if line == '[Term]':
        if id is not None:
            terms.append(Term(id=id,name=name,is_obsolete=is_obsolete,is_a=is_a))
            if not is_obsolete:
                G.add_node(id)
                for p in is_a:
                    G.add_edge(id,p)
        is_a = []
        is_obsolete = False
    if line.find(':') > 0:
        code, content = line.split(':',1)
        content = content.strip()
        if code == 'id':
            id = content
        elif code == 'name':
            name = content
        elif code == 'is_a':
            content,_ = content.split('!')
            content = content.strip()
            is_a.append(content)
        elif code == 'is_obsolete':
            is_obsolete = True

G.name = 'Gene Ontology'
cc_root = 'GO:0005575'
cellular_components = set(nx.search.dfs_tree(G,cc_root,reverse_graph=1).nodes())

