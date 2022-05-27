"""
Utility functions related to the generation and interpretation of the
Harte chord notation.
"""
from harte_map import GRADES_SHORTHAND_MAP
from typing import List

from music21 import chord, interval, note


def simplify_harte(harte_grades: List) -> str:
    """
    Utility function that given the grades that constitute a Harte chord
    (as a list) returns a string of Harte complained grades, using
    shorthands, if possible.
    Parameters
    ----------
    harte_grades : List
        A list of the grades as annotated in the Harte format, without
        any shortcut.
    Returns
    -------
    harte_attributes : str
        A list of the attributes formatted in Harte containing all the
        elements except for the bass note, using shorthands if possible.
        The output string has a format such as: :maj7(b9)
    """
    clean_harte_grades = clean_grades(harte_grades)
    separator, shorthand = '', ''
    for grades in GRADES_SHORTHAND_MAP.keys():
        intersection = set(grades).intersection(clean_harte_grades)
        if len(intersection) == len(grades):
            shorthand = GRADES_SHORTHAND_MAP[grades]
            clean_harte_grades = list(set(clean_harte_grades) - intersection)
            if 'sus' in shorthand and '*3' in clean_harte_grades:
                clean_harte_grades.remove('*3')
            break
    clean_harte_grades = f'({",".join([x for x in clean_harte_grades])})' if len(clean_harte_grades) > 0 else ''
    if len(shorthand) > 0 or len(clean_harte_grades) > 0:
        separator = ':'
    return separator + shorthand + clean_harte_grades


def calculate_interval(note_1: note, note_2: note, octave_1: int = 4, octave_2: int = 5, simple: bool = True) -> str:
    """
    Utility function that given two music21 notes returns the interval calculated
    between the two.
    Parameters
    ----------
    note_1 : music21.note.Note
        The start note from which the interval has to be calculated.
    note_2 : music21.note.Note
        The end note to which the interval has to be calculated.
    simple : bool
        To mode in which to return the function. If true the interval is printed
        in the music21 "simpleName" mode, in the "name" mode if False.
    Returns
    -------
    interval : str
        An interval as convention in the Harte notation (i.e. b for flat and #
        for sharp).
    """
    note_1.octave = octave_1
    note_2.octave = octave_2
    mode = 'simpleName' if simple is True else 'name'
    computed_interval = getattr(interval.Interval(note_1, note_2), mode)
    return convert_intervals(computed_interval).replace('b2', 'b9').replace('2', '9')


def convert_intervals(m21_interval: str) -> str:
    """
    Utility function that converts intervals from the music21 format to the Harte one.
    Parameters
    ----------
    m21_interval : str
        A string containing an interval as expressed by the music21 notation (e.g. 'P4').
    Returns
    -------
    harte:interval : str
        A string containing an interval as expressed by the Harte notation (e.g. 'b2').
    """
    substitutions = {
        'M': '',
        'm': 'b',
        'P': '',
        'd': 'b',
        'A': '#',
    }
    return m21_interval.translate(m21_interval.maketrans(substitutions))


def convert_root(chord_root: chord) -> str:
    """
    Utility function for cleaning the string of a chord root note and making
    it compliant to the Harte notation.
    Parameters
    ----------
    chord_root : music21.chord.Chord
        A chord expressed by the music21 notation.
    Returns
    -------
    harte_root : str
        The root of the note in the Harte notation.
    """
    root_note = str(chord_root)
    root = ''.join(x for x in root_note if not x.isdigit())
    return root.replace('-', 'b')


def clean_grades(grades_list: List) -> List:
    """
    Utility function that cleans and orders a list of tones encoded
    according to the Harte notation (containing 'b', '#', and '*').
    Parameters
    ----------
    grades_list : str
        A list of grades in the Harte notation.
        If the characters in input are illegal for the Harte notation,
        an exception is raised.
    Returns
    -------
    sorted_grades : str
        The input grades cleaned (without 1st and 8th grade, with *1
        if not root is listed among grades) sorted from the lower to
        the higher.
    """
    has_third = True if any("3" in g[-1] for g in grades_list) else False
    has_fifth = True if any("5" in g[-1] for g in grades_list) else False
    # add third and fifth if not in grades
    if not has_third:
        grades_list.append('*3')
    if not has_fifth:
        grades_list.append('*5')
    # pretty grades
    try:
        return sorted(grades_list, key=lambda x: int(x.replace('b', '').replace('#', '').replace('*', '')))
    except ValueError:
        raise ValueError('The list of grades contains non valid characters to the Harte notation.')
