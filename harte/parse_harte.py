import re
from pathlib import Path
from typing import Tuple

import more_itertools as mitertools
import numpy as np
from lark import Lark, Transformer
from music21.pitch import Pitch
from ordered_set import OrderedSet


with open(Path.cwd() / 'grammar' / "harte.lark", 'r') as g:
    HARTE_LARK_GRAMMAR = g.read()


class TreeToHarteTransformer(Transformer):
    """
    Lark transformer to turn a parse tree into an Harte chord representation.
    The representation consists of a dict with keys:
      * root
          Root note of the chord
      * shorthand - OPTIONAL
          Shorthand of the chord
      * bass - OPTIONAL
          Modified bass note if slash chord is used
      * degrees - OPTIONAL
          Modified degrees on the chord (with missing degrees identified with * i.e. *3
    """
    NATURAL = str
    MODIFIER = str
    MISSING = str
    SHORTHAND = lambda self, sh: {"shorthand": str(sh)}
    INTERVAL = str
    degree = lambda self, elems: "".join(elems)
    bass = lambda self, elems: {"bass": "".join(elems)}
    note = lambda self, elems: {"root": "".join(elems)}
    degree_list = lambda self, elems: elems

    def chord(self, elems):
        d = dict()
        for elem in elems:
            if isinstance(elem, dict):
                d.update(**elem)
            elif isinstance(elem, list):
                d.update({"degrees": list(mitertools.collapse(elem))})

        return d


PARSER = Lark(HARTE_LARK_GRAMMAR,
              parser='lalr',
              start="chord",
              propagate_positions=False,
              maybe_placeholders=False,
              transformer=TreeToHarteTransformer())

INTERVAL_RE = re.compile(r"(\d+)")
FLAT_RE = re.compile(r"(b)")
SHARP_RE = re.compile(r"(#)")
INTERVAL_MAP = {
    "1": 0,
    "2": 2,
    "3": 4,
    "4": 5,
    "5": 7,
    "6": 9,
    "7": 11,
    "8": 12,
    "9": 14,
    "10": 16,
    "11": 17,
    "13": 21
}


def degree_to_semitones(degree: str) -> int:
    """
    Convert a degree to its semitone distance from the root note.

    Args:
        degree (str): Degree in Harte format

    Returns:
        int: Semitones from the root note
    """
    numeric_degree = INTERVAL_RE.search(degree).group()
    numeric_degree = INTERVAL_MAP[numeric_degree]

    for _ in SHARP_RE.findall(degree): numeric_degree += 1
    for _ in FLAT_RE.findall(degree): numeric_degree -= 1

    return numeric_degree


def semitones_to_pitchclass(root: str, semitones: Tuple[int]) -> Tuple[int]:
    """
    Convert the number of semitones from the root to their pitchclass representation.

    Args:
        root (str): The root, relative to which the degrees will be computed.
        semitones (Tuple[int]): The semitones

    Returns:
        Tuple[int]: The pitchclass representation of the degrees, where C = 0, C# = 1, D = 2 ... B = 11.
    """
    root_pitch = Pitch(root)
    pitchclass = tuple(
        map(lambda d: root_pitch.transpose(d).pitchClass, semitones))
    return pitchclass


def chord_to_pitchclass(chord: str) -> Tuple[int]:
    """
    Convert an input chord into its pitchclass representation.

    Args:
        chord (str): Chord in Harte format

    Returns:
        Tuple[int]: Pitchclass representation
    """
    parsed = PARSER.parse(chord)

    if len(parsed) > 0:
        degrees = OrderedSet()

        # handle shorthand
        degrees.update(SHORTHAND_DEGREES[parsed.get("shorthand", "")])

        # handle additional degrees
        additional_degrees = parsed.get("degrees", [])
        to_add = filter(lambda d: "*" not in d, additional_degrees)
        to_remove = filter(lambda d: "*" in d, additional_degrees)
        # add additional degrees
        degrees.update(to_add)
        # remove degrees that are signaled using the "*"
        degrees = degrees.difference(
            map(lambda d: d.replace("*", ""), to_remove))

        # handle alternate bass
        if "bass" in parsed: degrees.add(parsed["bass"])

        # convert degrees to semitones and compute pitchclass
        semitones = map(degree_to_semitones, degrees)
        pitchclass = semitones_to_pitchclass(parsed["root"], tuple(semitones))
    else:
        pitchclass = []

    return tuple(pitchclass)


def pitchclass_to_onehot(pitchclass: Tuple[int]) -> np.array:
    """
    Convert a pitchclass representation to a one-hot encoding
    of a pitchclass representation: a 12-dimensional vector
    in which each dimension represents the respective pitchclass.

    Args:
        pitchclass (Tuple[int]): Pitchclass representation

    Returns:
        np.array: One hot encoding.
    """
    return np.eye(12)[pitchclass, :].sum(axis=0).clip(0, 1)


if __name__ == '__main__':
    # test the grammar parsed Tree
    print(PARSER.parse('C:maj7(4,b6)/b4'))
