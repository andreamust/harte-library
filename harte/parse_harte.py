"""
Parser for Harte chord data
"""

import os
from typing import Dict, List

import more_itertools as mitertools
from lark import Lark, Transformer

GRAMMAR = os.path.join(os.path.dirname(__file__), 'harte.lark')

with open(GRAMMAR, 'r', encoding='utf-8') as g:
    HARTE_LARK_GRAMMAR = g.read()


class TreeToHarteTransformer(Transformer):
    """
    Lark transformer to turn a parse tree into a Harte chord representation.
    The representation consists of a dict with keys:
      * root
          Root note of the chord
      * shorthand - OPTIONAL
          Shorthand of the chord
      * bass - OPTIONAL
          Modified bass note if slash chord is used
      * degrees - OPTIONAL
          Modified degrees on the chord (with missing degrees identified with *
           i.e. *3
    """
    @staticmethod
    def shorthand(shorthand: str) -> Dict[str, str]:
        """
        Extract the shorthand from the parse tree
        :param shorthand: shorthand of the chord
        :type shorthand: str
        :return: shorthand of the chord
        :rtype: str
        """
        return {"shorthand": str(shorthand[0])}

    @staticmethod
    def degree(degree: List[str]) -> str:
        """
        Extract the degree from the parse tree
        :param degree: degree of the chord
        :type degree: str
        :return: degree of the chord
        :rtype: str
        """
        return ''.join(degree)

    @staticmethod
    def bass(bass: List[str]) -> Dict[str, str]:
        """
        Extract the bass from the parse tree
        :param bass: bass of the chord
        :type bass: str
        :return: bass of the chord
        :rtype: str
        """
        return {'bass': ''.join(bass)}

    @staticmethod
    def note(root: List[str]) -> Dict[str, str]:
        """
        Extract the root from the parse tree
        :param root: root of the chord
        :type root: str
        :return: root of the chord
        :rtype: str
        """
        return {'root': ''.join(root)}

    @staticmethod
    def degree_list(degrees: List[str]) -> List[str]:
        """
        Extract the degrees from the parse tree
        :param degrees: degrees of the chord
        :type degrees: list
        :return: degrees of the chord
        :rtype: list
        """
        return degrees

    @staticmethod
    def chord(elements: List) -> Dict:
        """
        Method to transform a chord parse tree into a Harte chord representation
        :param elements: the chord parse tree
        :type elements: list
        :return: a Harte chord representation
        :rtype: dict
        """
        chord_dict = {}
        for elem in elements:
            if isinstance(elem, dict):
                chord_dict.update(**elem)
            elif isinstance(elem, list):
                chord_dict.update({"degrees": list(mitertools.collapse(elem))})

        return chord_dict


PARSER = Lark(HARTE_LARK_GRAMMAR,
              parser='lalr',
              start="chord",
              propagate_positions=False,
              maybe_placeholders=False,
              transformer=TreeToHarteTransformer())

if __name__ == '__main__':
    # test the grammar parsed Tree
    print(PARSER.parse('C:maj7(4,b6)/b4'))
