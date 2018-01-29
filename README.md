# dcs_wrapper

A small Python wrapper around the [Digital Corpus of Sanskrit](http://kjc-sv013.kjc.uni-heidelberg.de/dcs/index.php). Supports iterating through the books, chapters and grammatical analysis of sentences. The data contained as part of this project is based on the data available via [dcs_scraper](https://github.com/sanskrit-coders/dcs-scraper/) with some minor changes to correct unicode character encoding.

## Installation

`pip install dcs_wrapper`

## Usage

```python
>>> from dcs_wrapper import DCS
>>> with DCS() as dcs:
>>>     for book in dcs.iter_books():
>>>         print(book.dcsId, book.title)
>>>     for chapter in dcs.iter_chapters():
>>>         print(chapter.dcsId, chapter.dcsName)
>>>     for sentence in dcs.iter_sentences():
>>>         print(sentence.dcsId, sentence.text, sentence.dcsAnalysisDecomposition)
```

For more information, please see the docs at https://dcs-wrapper.readthedocs.io/en/latest/

## License

The code in this project is shared under the MIT license. 

The data is made available under the Creative Commons Attribution 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by/3.0/ . This is identical to the 
terms of the [DCS](http://kjc-sv013.kjc.uni-heidelberg.de/dcs/index.php?contents=impressum) and the [dcs_scraper](https://github.com/sanskrit-coders/dcs-scraper/blob/master/LICENSE.md) project.

## Acknowledgements

We are grateful to Prof. Oliver Hellwig for making the original data available on the website and the sanskrit programmers group for scraping the data in a suitable form. 