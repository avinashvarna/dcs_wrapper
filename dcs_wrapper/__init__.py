# -*- coding: utf-8 -*-
"""
A simple wrapper around the DCS database that supports iteration and tag conversion

"""

from .base import Book, Chapter, Sentence, WordAnalysis, from_json
from .wrapper import DCS
from .tags import DCSTagMapper

__all__ = [
        "DCS", "DCSTagMapper",
        "Book", "Chapter", "Sentence", "WordAnalysis", "from_json"
           ]
