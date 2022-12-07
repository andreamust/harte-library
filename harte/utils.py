"""

"""
import re


def convert_interval(harte_interval: str) -> str:
    """

    :param harte_interval: an interval of a Harte Chord
    :type harte_interval: str
    :return:
    """
    regex = r'([#]+)?([b]+)?(\d+)'
    matches = re.findall(regex, harte_interval)[0]

    base_degree = int(matches[2]) if int(matches[2]) < 8 else int(
        matches[2]) - 7

    if int(matches[2]) in [1, 4, 5]:
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
