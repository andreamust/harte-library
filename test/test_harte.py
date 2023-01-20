"""
Test cases for the harte module.
"""

import json
import os
from typing import List

import pytest

from harte.harte import Harte

# load a dict of chords frequencies extracted from ChoCo [1]
# to test coverage of a big set of chords
# [1] https://github.com/smashub/choco
CUR_DIR = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(CUR_DIR, "chords_count.json"), encoding="UTF-8") as f:
    CHORDS_COUNT = json.load(f)


@pytest.mark.parametrize("chord", list(CHORDS_COUNT.keys()))
def test_coverage(chord: str):
    """
    Tests coverage of all chord extracted from ChoCo [1].

    [1] https://github.com/smashub/choco

    :param chord: Chord to be tested
    :type chord: str
    """
    Harte(chord)


@pytest.mark.parametrize("chord,intervals",
                         [("C", ["P5", "M3"]),
                          ("A", ["P5", "M3"]),
                          ("C:maj", ["P5", "M3"]),
                          ("C:min", ["P5", "m3"]),
                          ("C:dim", ["d5", "m3"]),
                          ("C:aug", ["A5", "M3"]),
                          ("N", [])])
def test_interval_extraction(chord: str, intervals: List[str]):
    """
    Test that the annotateIntervals of music21 correctly works in extracting
    the intervals from a chord.

    :param chord: Input chord
    :type chord: str
    :param intervals: Intervals that should be part of the chord
    :type intervals: List[str]
    """
    chord = Harte(chord)
    annotated_intervals = chord.annotateIntervals(inPlace=False,
                                                  returnList=True,
                                                  stripSpecifiers=False)
    assert set(intervals) == set(annotated_intervals)


@pytest.mark.parametrize("chord,pitches", [("F:(b3, 5, b7, 11)",
                                            ["F", "A-", "C", "E-", "B-"]),
                                           ("F:(b3, 11, b7, 5)",
                                            ["F", "A-", "C", "E-", "B-"]),
                                           ("F:maj7(#11)",
                                            ["F", "A", "C", "E", "B"])])
def test_ordering_of_degrees(chord: str, pitches: List[str]):
    """
    Test that the parsed degrees are ordered correctly in the resulting m21 object.

    :param chord: Input chord
    :type chord: str
    :param pitches: Pitches that should be part of the chord
    :type pitches: List[str]
    """
    chord = Harte(chord)
    assert [p.name for p in chord.pitches] == pitches
