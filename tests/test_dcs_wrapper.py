# -*- coding: utf-8 -*-
"""
Simple test for dcs wrapper

@author: avinashvarna
"""
import pytest
from indic_transliteration import sanscript
from dcs_wrapper import DCS, Book, Chapter, Sentence, DCSTagMapper


@pytest.fixture(scope="module")
def dcs():
    return DCS()


@pytest.fixture(scope="module")
def mapper():
    return DCSTagMapper()


def to_SLP1(x):
    return sanscript.transliterate(x, sanscript.DEVANAGARI, sanscript.SLP1)


def test_books(dcs):
    for book in dcs.iter_books():
        assert type(book) == Book
        break


def test_chapters(dcs):
    for chapter in dcs.iter_chapters():
        assert type(chapter) == Chapter
        break


def test_sentences(dcs):
    for sentence in dcs.iter_sentences():
        assert type(sentence) == Sentence
        break


def test_mapper(mapper):
    assert mapper.map_tag("ac.p.f") == set(map(to_SLP1, {'स्त्रीलिङ्गम्', 'द्वितीयाविभक्तिः', 'बहुवचनम्'}))
    assert mapper.map_tag("3. pl. Proh.") == set(map(to_SLP1, {'प्रथमपुरुषः', 'बहुवचनम्', 'आगमाभावयुक्तलुङ्'}))
