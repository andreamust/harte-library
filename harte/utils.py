"""

"""
import re
from typing import List

from harte.mappings import SHORTHAND_DEGREES


def convert_interval(harte_interval: str) -> str:
    """
    TBD
    :param harte_interval: an interval of a Harte Chord
    :type harte_interval: str
    :return:
    """
    regex = r'([#]+)?([b]+)?(\d+)'
    matches = re.findall(regex, harte_interval)[0]

    base_degree = int(matches[2]) if int(matches[2]) < 8 else int(
        matches[2]) - 7

    if base_degree in [1, 4, 5]:
        if len(matches[0]) == 0 and len(matches[1]) == 0:
            modifier = 'P'
        elif len(matches[1]) == 1 and len(matches[0]) == 0:
            modifier = 'A'
        elif len(matches[0]) == 1 and len(matches[1]) == 0:
            modifier = 'd'
        else:
            raise ValueError(f'The degree {harte_interval} cannot '
                             f'be parsed.')
    else:
        if len(matches[0]) == 0 and len(matches[1]) == 0:
            modifier = 'M'
        elif len(matches[0]) == 1 and len(matches[1]) == 0:
            modifier = 'A'
        elif len(matches[1]) == 1 and len(matches[0]) == 0:
            modifier = 'm'
        elif len(matches[1]) == 2 and len(matches[0]) == 0:
            modifier = 'd'
        else:
            raise ValueError(f'The degree {harte_interval} cannot '
                             f'be parsed.')

    return modifier + str(base_degree)


def unwrap_shorthand(harte_shorthand: str, harte_degrees: list) -> List[str]:
    """
    TBD
    :param harte_shorthand:
    :type harte_shorthand: str
    :param harte_degrees:
    :type harte_degrees: list
    :return:
    """
    if harte_degrees or len(harte_degrees) > 0 and harte_shorthand != '':
        pass
    assert harte_shorthand in SHORTHAND_DEGREES.keys(), 'The Harte shorthand ' \
                                                        'is not valid. '

    shorthand_degrees = SHORTHAND_DEGREES[harte_shorthand]
    degrees = list(set(shorthand_degrees + harte_degrees))
    degrees.sort(key=lambda x: [k for k in x if k.isdigit()][0])
    return degrees


if __name__ == '__main__':
    print(unwrap_shorthand('minmaj9', ['b7', 'b9']))
