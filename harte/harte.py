import os
import re
from typing import Tuple
from  pathlib import Path

import more_itertools as mitertools
import numpy as np
from music21.pitch import Pitch
from ordered_set import OrderedSet

from lark import Lark, Transformer

SHORTHAND_DEGREES = {
    "": ["1", "3", "5"],
    "maj": ["1", "3", "5"],
    "min": ["1", "b3", "5"],
    "aug": ["1", "3", "#5"],
    "dim": ["1", "b3", "b5"],
    "7": ["1", "3", "5", "b7"],
    "maj7": ["1", "3", "5", "7"],
    "minmaj7": ["1", "b3", "5", "7"],
    "min7": ["1", "b3", "5", "b7"],
    "augmaj7": ["1", "3", "#5", "7"],
    "aug7": ["1", "3", "#5", "b7"],
    "hdim7": ["1", "b3", "b5", "b7"],
    "dim7": ["1", "b3", "b5", "bb7"],
    "dom7dim5": ["1", "3", "b5", "b7"],
    "maj6": ["1", "3", "5", "6"],
    "min6": ["1", "b3", "5", "6"],
    "maj9": ["1", "3", "5", "7", "9"],
    "9": ["1", "3", "5", "b7", "9"],
    "minmaj9": ["1", "b3", "5", "7", "9"],
    "min9": ["1", "b3", "5", "b7", "9"],
    "augmaj9": ["1", "3", "#5", "7", "9"],
    "aug9": ["1", "3", "#5", "b7", "9"],
    "hdim9": ["1", "b3", "b5", "b7", "9"],
    "hdimmin9": ["1", "b3", "b5", "b7", "b9"],
    "dim9": ["1", "b3", "b5", "bb7", "9"],
    "dimmin9": ["1", "b3", "b5", "bb7", "b9"],
    "11": ["1", "3", "5", "b7", "9", "11"],
    "maj11": ["1", "3", "5", "7", "9", "11"],
    "minmaj11": ["1", "b3", "5", "7", "9", "11"],
    "min11": ["1", "b3", "5", "b7", "9", "11"],
    "augmaj11": ["1", "3", "#5", "7", "9", "11"],
    "aug11": ["1", "3", "#5", "b7", "9", "11"],
    "hdim11": ["1", "b3", "b5", "b7", "b9", "11"],
    "dim11": ["1", "b3", "b5", "bb7", "b9", "b11"],
    "maj13": ["1", "3", "5", "7", "9", "11", "13"],
    "13": ["1", "3", "5", "b7", "9", "11", "13"],
    "minmaj13": ["1", "b3", "5", "7", "9", "11", "13"],
    "min13": ["1", "b3", "5", "b7", "9", "11", "13"],
    "augmaj13": ["1", "3", "#5", "7", "9", "11", "13"],
    "hdim13": ["1", "b3", "b5", "b7", "9", "11", "13"],
    "sus2": ["1", "2", "5"],
    "sus4": ["1", "4", "5"],
    "7sus4": ["1", "4", "5", "b7"],
    "power": ["1", "5"],
    "pedal": ["1", ]
}

with open(Path.cwd()/'grammar'/"harte.lark", 'r') as g:
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
    print(HARTE_LARK_GRAMMAR)
