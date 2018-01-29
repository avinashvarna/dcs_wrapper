'''
A simple wrapper around the DCS database that supports iteration

@author: avinashvarna
'''

from __future__ import print_function
import os
import logging
import codecs
import tarfile

try:
    from functools import partialmethod
except ImportError:
    from backports.functools_partialmethod import partialmethod


from .base import from_json
from .utils import app_dir


__docformat__ = 'reStructuredText'


class DCS(object):
    '''Simple wrapper around the DCS database supporting iteration

    :param file_path: Use the data in directory file_path.
        file_path = None defaults to using data supplied with the package
        which will be extracted on first use
    :type file_path: str, None

    :Example:

    >>> from dcs_wrapper import DCS
    >>> with DCS() as dcs:
    >>>     for book in dcs.iter_books():
    >>>         print(book.dcsId, book.title)
    >>>     for chapter in dcs.iter_chapters():
    >>>         print(chapter.dcsId, chapter.dcsName)
    >>>     for sentence in dcs.iter_sentences():
    >>>         print(sentence.dcsId, sentence.text)


    '''

    def __init__(self, file_path=None):
        self.logger = logging.getLogger(__name__)
        self._setup_directory(file_path)

    def _setup_directory(self, file_path):
        data_file = os.path.join(os.path.dirname(__file__),
                                 "data", "dcs_data.tar.gz")
        self.file_path = file_path or app_dir('DCS_Wrapper')
        self.sentences_file = os.path.join(self.file_path, 'dcs_sentences_json.txt')
        self.books_file = os.path.join(self.file_path, 'dcs_books_json.txt')
        self.chapters_file = os.path.join(self.file_path, 'dcs_chapters_json.txt')
        file_list = [self.books_file, self.chapters_file, self.sentences_file]
        if not all(map(os.path.exists, file_list)):
            self.logger.info("Unzipping data files for first use")
            with tarfile.open(data_file, 'r') as tar:
                tar.extractall(self.file_path)
        assert all(map(os.path.exists, file_list)), "One of %s does not exist" % (file_list)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _iter_file(self, category):
        if category == "books":
            filename = self.books_file
        elif category == "chapters":
            filename = self.chapters_file
        elif category == "sentences":
            filename = self.sentences_file
        with codecs.open(filename, "rb", "utf8") as f:
            for line in f:
                yield from_json(line)

    iter_sentences = partialmethod(_iter_file, "sentences")
    '''Iterate over sentences in DCS database, yielding one :class:`~dcs_wrapper.Sentence` at a time'''

    iter_books = partialmethod(_iter_file, "books")
    '''Iterate over books in DCS database, yielding one :class:`~dcs_wrapper.Book` at a time'''

    iter_chapters = partialmethod(_iter_file, "chapters")
    '''Iterate over chapters in DCS database, yielding one :class:`~dcs_wrapper.Chapter` object at a time'''
