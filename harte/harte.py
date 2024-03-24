"""
Extension of the Chord class from music21.chord to support the
Harte notation.
"""

# pylint: disable=consider-using-dict-items
from typing import List, Union

from music21.chord import Chord, ChordException
from music21.note import Note

from harte.interval import HarteInterval
from harte.mappings import SHORTHAND_DEGREES, DEGREE_SHORTHAND_MAP
from harte.parse_harte import PARSER
from harte.utils import degree_to_sort_key


class Harte(Chord):
    """
    Extension of the Chord class from music21.chord to support the
    Harte notation.
    """

    def __init__(self, chord: str, **keywords):
        """
        Constructor for the Harte class. It takes a Harte chord as input
        and parses it to extract the root, bass, degrees and shorthand. The
        constructor of the Chord class is then called to create the chord
        object
        :param chord: a music chord annotated according to the Harte notation
        :type chord: str
        """
        self.chord = chord
        self._root = None
        self._bass = None
        self._all_degrees = ["1"]
        self._shorthand = []
        self._degrees = []
        self._shorthand_degrees = []

        # parse the chord
        try:
            parsed_chord = PARSER.parse(chord)
        except NameError as name_error:
            raise ChordException(
                f"The input chord {chord} is not a valid Harte chord"
            ) from name_error

        # chord is not empty
        if "root" in parsed_chord:
            # retrieve information from the parsed chord
            self._root = parsed_chord["root"]
            self._shorthand = parsed_chord.get("shorthand", None)
            self._degrees = parsed_chord.get("degrees", [])
            self._bass = parsed_chord.get("bass", "1")
            removed_degrees = (
                [x.replace("*", "") for x in self._degrees if x.startswith("*")]
                if self._degrees
                else []
            )

            # unwrap shorthand if it exists and merge with degrees
            if self._shorthand:
                assert SHORTHAND_DEGREES[
                    self._shorthand
                ], "The Harte shorthand is not valid."
                self._shorthand_degrees = SHORTHAND_DEGREES[self._shorthand]
                self._all_degrees += self._shorthand_degrees + self._degrees
            # if no shorthand exists, just use the degrees
            elif self._degrees and len(self._degrees) > len(removed_degrees):
                self._all_degrees += self._degrees
            # if no degrees exist, assume the chord is a major triad
            else:
                self._all_degrees += ["3", "5"]

            # remove the degrees included in removed_degrees and the ones that start with '*'
            self._all_degrees = [
                x
                for x in set(self._all_degrees)
                if x not in removed_degrees and x[0] != "*"
            ]
            # add root and bass note to the overall list of degrees
            self._all_degrees.append(self._bass)

            # sort the list and remove duplicates
            self._all_degrees = list(set(self._all_degrees))
            self._all_degrees.sort(key=degree_to_sort_key)

            # convert notes and interval to m21 primitives
            # note that when multiple flats are introduced (i.e. Cbb) music21
            # won't be able to parse the note.
            # this is fixed by replacing each 'b' with a '-'.
            m21_root = Note(self._root.replace("b", "-"), octave=4)
            m21_degrees = [
                HarteInterval(x, octave=4).transposeNote(m21_root)
                for x in self._all_degrees
            ]
            m21_bass = HarteInterval(self._bass).transposeNote(m21_root)
            if m21_root != m21_bass:
                m21_bass.octave = 3

            # initialize the parent constructor
            super().__init__(m21_degrees, **keywords)
            super().root(m21_root)
            super().bass(m21_bass)
            # set octave of root and bass to 4 and 3 respectively
            super().bass().octave = 3
            super().root().octave = 4

        else:
            # chord is empty
            super().__init__()

    def __deepcopy__(self, *args, **kwargs):
        """
        Perform a deepcopy of this object by creating a new identical
        object with the input chord used for this one.

        :return: A copy of the current object.
        :rtype: Harte
        """
        return Harte(self.chord)

    def get_degrees(self) -> List[str]:
        """
        Method to retrieve the degrees of the chord in Harte notation without
        considering the degrees associated to the shorthand
        :return: a list of strings representing the degrees of the chord in
        Harte notation (e.g. ['b3', '5', '7'])
        :rtype: list[str]
        """
        return self._degrees if self._degrees else None

    def get_midi_pitches(self) -> List[int]:
        """
        Method to retrieve the MIDI pitches of the chord
        :return: a list of integers representing the MIDI pitches of the chord
        """
        return sorted([x.midi for x in self.pitches])

    def multi_hot_encoding(self, transpose: bool = False) -> List[int]:
        """
        Method to retrieve the multi-hot encoding of the chord in Harte notation.
        The multi-hot encoding is a list of integers where each integer is 1 if
        the corresponding pitch is present in the chord, 0 otherwise
        :return: a list of integers representing the multi-hot encoding of the
        chord in Harte notation
        """
        pitch_classes = [x.pitchClass for x in self.pitches]
        if transpose:
            # get the pitch class of the root note
            root_pitch_class = self.root().pitchClass
            # transpose the chord so that the root note is at the 0th position
            pitch_classes = [(x - root_pitch_class) % 12 for x in pitch_classes]
        return [1 if i in pitch_classes else 0 for i in range(12)]

    def get_root(self) -> str:
        """
        Method to retrieve the root of the chord in Harte notation expressed as
        a string representing the note name (e.g. 'C#')
        :return: the root of the chord expressed as a string representing the
        note name (e.g. 'C#')
        :rtype: str
        """
        return self._root if self._root else None

    def get_bass(self) -> str:
        """
        Method to retrieve the bass of the chord in Harte notation expressed as
        a string representing the note interval calculated from the root note
        (e.g. 'b3)
        :return: the bass of the chord expressed as a string representing the
        note interval calculated from the root note (e.g. 'b3)
        """
        return self._bass if self._bass else None

    def bass_is_root(self) -> bool:
        """
        Method to check if the bass of the chord is the same as the root of the
        chord
        :return: True if the bass of the chord is the same as the root of the
        chord, False otherwise
        :rtype: bool
        """
        return self._root == self._bass

    def contains_shorthand(self) -> bool:
        """
        Method to check if the chord contains a shorthand or not
        :return: True if the chord contains a shorthand notation, False
        otherwise
        :rtype: bool
        """
        return self._shorthand is not None

    def get_shorthand(self) -> Union[str, bool]:
        """
        Method to retrieve the shorthand of the chord in Harte notation
        :return: the shorthand of the chord in Harte notation (e.g. 'maj7')
        if it exists, None otherwise
        :rtype: str
        """
        return self._shorthand

    def prettify(self) -> str:
        """
        Method to prettify the chord in Harte notation. It decomposes the chord
        into its constituent parts and returns a string representing the chord
        in Harte notation summarising the constituent degrees in shorthands,
        if possible
        :return: a string representing the chord in Harte notation summarising
        the constituent degrees in shorthands, if possible. If it is not
        possible to summarise the chord in a shorthand, the chord is returned
        in its original form
        :rtype: str
        """
        separator, shorthand = None, None
        assert self._all_degrees, "The chord is empty: no degrees to prettify."
        degrees = self._all_degrees
        if "1" in degrees:
            degrees.remove("1")
        for grades in DEGREE_SHORTHAND_MAP.keys():
            intersection = set(grades).intersection(degrees)
            if len(intersection) == len(grades):
                shorthand = DEGREE_SHORTHAND_MAP[grades]
                clean_harte_degrees = list(set(degrees) - intersection)
                if "sus" in shorthand and "*3" in clean_harte_degrees:
                    clean_harte_degrees.remove("*3")
                break
        if shorthand:
            clean_harte_degrees = (
                f'({",".join(clean_harte_degrees)})'
                if len(clean_harte_degrees) > 0
                else ""
            )
            if len(shorthand) > 0 or len(clean_harte_degrees) > 0:
                separator = ":"

            bass = f"/{self._bass}" if self._bass != "1" else ""
            return self._root + separator + shorthand + clean_harte_degrees + bass
        return self.chord

    def unwrap_shorthand(self) -> Union[List[str], None]:
        """
        Method to retrieve the degrees of the chord in Harte notation, both
        those associated to the shorthand and those explicitly specified
        :return: a list of strings representing the degrees of the chord in
        Harte notation, both those associated to the shorthand and those
        explicitly specified.
        """
        if self._shorthand:
            return self._all_degrees
        if self._degrees:
            return self._degrees
        return None

    def __eq__(self, other):
        """
        Method to check if two HarteChord objects are equal
        :param other: the other HarteChord object to compare to the current
        object
        :return: True if the two HarteChord objects are equal, False otherwise
        """
        if isinstance(other, Harte):
            return (
                self._root == other.get_root()
                and self._degrees == other.get_degrees()
                and self._bass == other.get_bass()
            )
        return False

    def __repr__(self):
        """
        Method to represent the HarteChord object as a string
        :return: a string representing the HarteChord object
        """
        return f"Harte({str(self)})"

    def __str__(self):
        """
        Method to represent the HarteChord object as a string
        :return: a string representing the HarteChord object
        """
        if self._root is not None:
            chord_str = self._root
            if self._shorthand is not None:
                chord_str += ":" + self._shorthand
            if self._degrees is not None:
                chord_str += "(" + self._degrees + ")"
            if self._bass != "1":
                chord_str += "/" + self._bass
        else:
            chord_str = "N"

        return chord_str
