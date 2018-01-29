# -*- coding: utf-8 -*-
"""
Map DCS tags to a common interface

@author: alvarna
"""

from __future__ import print_function
# import codecs
import logging
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache
from indic_transliteration import sanscript


vibhakti_map = {
        'n':  'प्रथमाविभक्तिः',
        'ac': 'द्वितीयाविभक्तिः',
        'i':  'तृतीयाविभक्तिः',
        'd':  'चतुर्थीविभक्तिः',
        'ab': 'पञ्चमीविभक्तिः',
        'g':  'षष्ठीविभक्तिः',
        'l':  'सप्तमीविभक्तिः',
        'v': 'संबोधनविभक्तिः'
        }

vachana_map = {
        's': 'एकवचनम्',
        'd': 'द्विवचनम्',
        'p': 'बहुवचनम्',
        'sg': 'एकवचनम्',
        'du': 'द्विवचनम्',
        'pl': 'बहुवचनम्'
        }

linga_map = {
        'm': 'पुंल्लिङ्गम्',
        'f': 'स्त्रीलिङ्गम्',
        'n': 'नपुंसकलिङ्गम्',
        'a': 'त्रिलिङ्गम्'
        }

purusha_map = {
        '1': 'उत्तमपुरुषः',
        '2': 'मध्यमपुरुषः',
        '3': 'प्रथमपुरुषः'
        }

lakaara_map = {
        'Ind': 'लट्',
        'root Aor': 'लुङ्',
        'Impf': 'लङ्',
        'Perf': 'लिट्',
        'Fut': 'लृट्',
        'periphr. Fut': 'लुट्',
        'Cond': 'लृङ्',
        'Opt. Pr': 'विधिलिङ्',
        'Imper': 'लोट्',
        'Prec': 'आशीर्लिङ्',
        'Proh': 'आगमाभावयुक्तलुङ्',
        'Aor': 'लुङ्',
        'them. Aor': 'लुङ्',
        'Opt. P': 'विधिलिङ्',
        'athem. is-Aor': 'लुङ्',
        'athem. s-Aor': 'लुङ्',
        'sa-Aor': 'लोट्',
        'periphr. Perf': 'लिट्',
        # 'redupl. Aor':
        }

misc_tag_map = {
        'Abs': {'क्त्वा'},
        # FIXME
        'Fut': {'कर्तरिभविष्यत्कृदन्त'},
        'Ger': {'कर्मणिभविष्यत्कृदन्तः'},
        'Imper. Pass': {'लोट्', 'कर्मणि'},
        'Imper. Pr': {'लोट्'},
        'Ind. Pass': {'लट्', 'भावे'},
        'Ind. Pr': {'लट्'},
        'Inf': {'तुमुन्'},
        'Opt. Pr': {'विधिलिङ्'},
        'PP': {'भूतकृदन्तः'},
        'Perf': {'लिट्'},
        'comp': {'समासपूर्वपदनामपदम्'},
        'indecl': {'अव्ययम्'},
        'them. Aor': {'लुङ्'},
        'not se': None,
        }

logger = logging.getLogger(__name__)


def to_slp1(s):
    return sanscript.transliterate(s, sanscript.DEVANAGARI, sanscript.SLP1)


class DCSTagMapper(object):

    @staticmethod
    def _map_nominal(tag):
        '''Map tags for nominal words'''
        # Remove the extra annotation for ShaShTI
        tag = tag.replace("/o.", "")
        tags = set()
        dcs_tags = list(map(str.strip, tag.split(".")))
        vibhakti = dcs_tags.pop(0)
        if vibhakti in vibhakti_map:
            tags.add(vibhakti_map[vibhakti])
        else:
            logger.debug("vibhakti map not found for %s", vibhakti)
        vachana = dcs_tags.pop(0)
        if vachana in vachana_map:
            tags.add(vachana_map[vachana])
        else:
            logger.debug("vachana map not found for %s", vachana)
        if len(dcs_tags) > 0:
            linga = dcs_tags.pop(0)
            if linga in linga_map:
                tags.add(linga_map[linga])
            else:
                logger.debug("linga map not found for %s", linga)
        if len(dcs_tags) != 0:
            logger.debug("Remaining nominal tags = %s", dcs_tags)
        return tags

    @staticmethod
    def _map_verb(tag):
        '''Map tags for verb forms'''
        tags = set()
        dcs_tags = list(map(str.strip, tag.split(".")))
        purusha = dcs_tags.pop(0)
        if purusha in purusha_map:
            tags.add(purusha_map[purusha])
        else:
            logger.debug("puruSha map not found for %s", purusha)
        vachana = dcs_tags.pop(0)
        if vachana in vachana_map:
            tags.add(vachana_map[vachana])
        else:
            logger.debug("vachana map not found for %s", vachana)
        lakaara = dcs_tags.pop(0)
        if lakaara not in lakaara_map:
            if len(dcs_tags) > 0:
                lakaara += '. ' + dcs_tags.pop(0).strip()
        if lakaara in lakaara_map:
                tags.add(lakaara_map[lakaara])
        else:
            logger.debug('lakaara map not found for %s', lakaara)
        if (lakaara == 'Ind' or lakaara == 'Imper') and dcs_tags[0] == 'Pr':
            dcs_tags.pop(0)
        if len(dcs_tags) > 0 and dcs_tags[0] == 'Pass':
            tags.add('कर्मणि')
            dcs_tags.pop(0)
        if len(dcs_tags) != 0:
            logger.debug("Remaining verb tags = %s", dcs_tags)
        return tags

    @staticmethod
    @lru_cache(200)
    def map_tag(tag):
        ''' Map tags to a human readable format

        :param tag: Tag from DCS database
        :type tag: str
        :return: Set of human readable tags in devanagari
        :rtype: set
        '''
        first = tag.split(".")[0]
        tags = None
        if first in vibhakti_map:
            tags = DCSTagMapper._map_nominal(tag)
        if first in purusha_map:
            tags = DCSTagMapper._map_verb(tag)
        if tag in misc_tag_map:
            tags = misc_tag_map[tag]
        if tags is not None:
            return set(map(to_slp1, tags))
        logger.debug("map not found for %s", tag)
        return None


if __name__ == "__main__":
    # Extract all the tags in DCS data
    # tags = defaultdict(set)
    # with DCS(reduce_memory=True) as dcs:
    #    for i, sent in enumerate(dcs.iter_sentences()):
    #        for group in sent.analysis:
    #            for word_analysis in group:
    #                if 'dcsGrammarHint' in word_analysis:
    #                    tags[word_analysis['dcsGrammarHint'][1:-2]].add(sent)
    #        if i == 10:
    #            break

    # with open('dcs_tags.txt', 'w') as f:
    #    for tag in tags:
    #        f.write(tag + "\n")

    #     tag_mapper = DCSTagMapper().map_tag
    #     with open('dcs_tags.txt', 'r') as fin, \
    #             codecs.open('dcs_tags_mapped.txt', 'wb', 'utf-8') as fout:
    #         for i, line in enumerate(fin):
    #             # print(i)
    #             line = line.strip()
    #             fout.write(line + " --> " + str(tag_mapper(line)) + "\n")
    pass
