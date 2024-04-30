"""
Test the HarteInterval class
"""

import pytest

from harte.utils import convert_interval


@pytest.mark.parametrize(
    "harte_interval,music21_interval",
    [
        ("b1", "d1"),
        ("1", "P1"),
        ("#1", "A1"),
        ("b2", "m2"),
        ("2", "M2"),
        ("#2", "A2"),
        ("b3", "m3"),
        ("3", "M3"),
        ("#3", "A3"),
        ("b4", "d4"),
        ("4", "P4"),
        ("#4", "A4"),
        ("b5", "d5"),
        ("5", "P5"),
        ("#5", "A5"),
        ("b6", "m6"),
        ("6", "M6"),
        ("#6", "A6"),
        ("b7", "m7"),
        ("7", "M7"),
        ("#7", "A7"),
        ("b8", "d1"),
        ("8", "P1"),
        ("#8", "A1"),
        ("b9", "m2"),
        ("9", "M2"),
        ("#9", "A2"),
        ("b10", "m3"),
        ("10", "M3"),
        ("#10", "A3"),
        ("b11", "d4"),
        ("11", "P4"),
        ("#11", "A4"),
        ("b12", "d5"),
        ("12", "P5"),
        ("#12", "A5"),
        ("b13", "m6"),
        ("13", "M6"),
        ("#13", "A6"),
        ("b14", "m7"),
        ("14", "M7"),
        ("#14", "A7"),
    ],
)
def test_harte_interval(harte_interval: str, music21_interval: str):
    """
    Test the conversion of Harte intervals to music21 intervals
    :param harte_interval: Harte interval
    :type harte_interval: str
    :param music21_interval: music21 interval
    :type music21_interval: str
    """
    harte_interval = convert_interval(harte_interval)

    assert harte_interval == music21_interval
