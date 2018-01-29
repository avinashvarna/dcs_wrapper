# -*- coding: utf-8 -*-
"""
Base classes and utilities

@author: avinashvarna
"""

from __future__ import print_function
from collections import namedtuple
import six

try:
    import ujson as json
except ImportError:
    import json


Book = namedtuple("Book", ["dcsId", "title", "chapterIds"])
''' Represents a book in the DCS database
'''
if not six.PY2:
    Book.dcsId.__doc__ = '''ID of the book in DCS'''
    Book.title.__doc__ = '''Title of the book'''
    Book.chapterIds.__doc__ = '''List of IDs of chapters in the book'''


Chapter = namedtuple("Chapter", ["dcsId", "dcsName", "sentenceIds"])
''' Represents a chapter in the DCS database
'''
if not six.PY2:
    Chapter.dcsId.__doc__ = '''ID of the chapter in DCS'''
    Chapter.dcsName.__doc__ = '''Name of the chapter in DCS'''
    Chapter.sentenceIds.__doc__ = '''List of IDs of sentences in the book'''

Sentence = namedtuple("Sentence",
                      ['dcsId', 'text', 'dcsAnalysisDecomposition'])
''' Represents a Sentence in the DCS database
'''
if not six.PY2:
    Sentence.dcsId.__doc__ = '''ID of the sentence in DCS'''
    Sentence.text.__doc__ = '''IAST encoded unicode string of the actual text'''
    Sentence.dcsAnalysisDecomposition.__doc__ = \
        '''Grammatical analysis of each word represented as
        list(list(:class:`~dcswrapper.WordAnalysis`))
        '''

WordAnalysis = namedtuple("WordAnalysis",
                          ['dcsId', 'root', 'dcsGrammarHint'])
''' Represents the analysis of a word in the DCS database
'''
if not six.PY2:
    WordAnalysis.dcsId.__doc__ = '''ID of the lemma in DCS'''
    WordAnalysis.root.__doc__ = '''IAST encoded unicode lemma/root of the word'''
    WordAnalysis.dcsGrammarHint.__doc__ = '''Grammatical analysis of each word'''


def from_json(s):
    ''' Convert a json string into an object of DCS wrapper

    Looks at the jsonClass type hint in the json string to determine
    the type of object to return

    :param s: JSON string
    :type s: str
    :return: Book, Chapter or Sentence depending on the encoded object
    :rtype: :class:`~dcswrapper.Book`, :class:`~dcswrapper.Chapter`, :class:`~dcswrapper.Sentence`
    '''
    d = json.loads(s)
    jsonClass = d.pop("jsonClass")
    if jsonClass == "DcsBook":
        return Book(**d)
    if jsonClass == "DcsChapter":
        return Chapter(**d)
    if jsonClass == "DcsSentence":
        decomp = d['dcsAnalysisDecomposition']
        decomp_obj = []
        for l in decomp:
            curr = []
            for w in l:
                curr.append(WordAnalysis(**w))
            decomp_obj.append(curr)
        d['dcsAnalysisDecomposition'] = decomp_obj
        return Sentence(**d)
