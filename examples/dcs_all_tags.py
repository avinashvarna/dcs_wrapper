# -*- coding: utf-8 -*-
"""
Find unique tags in DCS database

@author: alvarna
"""

from __future__ import print_function
import time

from dcs_wrapper import DCS

start = time.time()

tags = set()
with DCS() as dcs:
    for i, sent in enumerate(dcs.iter_sentences()):
        for group in sent.dcsAnalysisDecomposition:
            for word_analysis in group:
                tag = word_analysis.dcsGrammarHint.replace("[", "").replace("]", "")
                tags.add(tag)

print("Found %d unique tags" % len(tags))

with open("tags.txt", "w") as fp:
    fp.write("\n".join(sorted(tags)))

end = time.time()
print("Took %0.2f seconds" % (end-start))
