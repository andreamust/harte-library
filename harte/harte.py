"""

"""

from harte.interval import HarteInterval
from harte.mappings import SHORTHAND_DEGREES, DEGREE_SHORTHAND_MAP
from harte.parse_harte import PARSER
from music21.chord import Chord, ChordException
from music21.note import Note


class Harte(Chord):
    """

    """

    def __init__(self, chord: str, **keywords):
        """

        :param chord:
        :type chord: str
        """
        self.chord = chord
        try:
            parsed_chord = PARSER.parse(chord)
        except NameError:
            raise ChordException(
                f'The input chord {chord} is not a valid Harte chord')

        assert parsed_chord['root']

        # retrieve information from the parsed chord
        self._root = parsed_chord['root']
        self._shorthand = parsed_chord[
            'shorthand'] if 'shorthand' in parsed_chord.keys() else None
        self._degrees = parsed_chord[
            'degrees'] if 'degrees' in parsed_chord.keys() else None
        self._bass = parsed_chord[
            'bass'] if 'bass' in parsed_chord.keys() else '1'
        self._removed_degrees = [x for x in self._degrees if x.startswith(
            '*')] if self._degrees else []

        # unwrap shorthand if it exists and merge with degrees
        # if no shorthand exists, just use the degrees
        # if no degrees exist, assume the chord is a major triad
        if self._shorthand:
            assert self._shorthand in SHORTHAND_DEGREES.keys(), 'The Harte ' \
                                                                'shorthand is' \
                                                                ' not valid. '
            self._shorthand_degrees = SHORTHAND_DEGREES[self._shorthand]
            self._all_degrees = self._shorthand_degrees + self._degrees if self._degrees else self._shorthand_degrees
        elif self._degrees:
            self._all_degrees = self._degrees
        else:
            self._all_degrees = ['1', '3', '5']

        self._all_degrees = [x for x in self._all_degrees if
                             x not in self._removed_degrees]
        # add root and bass note to the overall list of degrees
        self._all_degrees.append(self._bass)
        self._all_degrees.append('1')
        # sort the list and remove duplicates
        self._all_degrees.sort(key=lambda x: [k for k in x if k.isdigit()][0])
        self._all_degrees = list(set(self._all_degrees))

        # convert notes and interval to m21 primitives
        self._m21_root = Note(self._root)
        self._m21_degrees = [HarteInterval(x).transposeNote(self._m21_root)
                             for x in self._all_degrees]
        self._m21_bass = HarteInterval(self._bass).transposeNote(
            self._m21_root)

        # initialize the parent constructor
        super().__init__(self._m21_degrees, **keywords)
        super().root(self._m21_root)
        super().bass(self._m21_bass)

    def get_degrees(self) -> list[str]:
        """

        :return:
        """
        return self._degrees

    def get_root(self) -> str:
        """

        :return:
        """
        return self._root

    def get_bass(self) -> str:
        """

        :return:
        """
        return self._bass

    def bass_is_root(self) -> bool:
        """

        :return:
        """
        if self._bass == self._root:
            return True
        return False

    def contains_shorthand(self) -> bool:
        """

        :return:
        """
        if self._shorthand:
            return True
        return False

    def get_shorthand(self) -> str:
        """

        :return:
        """
        return self._shorthand

    def prettify(self) -> str:
        """

        :return:
        """
        separator, shorthand = None, None
        degrees = self._all_degrees
        if '1' in degrees:
            degrees.remove('1')
        for grades in DEGREE_SHORTHAND_MAP.keys():
            intersection = set(grades).intersection(degrees)
            if len(intersection) == len(grades):
                shorthand = DEGREE_SHORTHAND_MAP[grades]
                clean_harte_degrees = list(
                    set(degrees) - intersection)
                if 'sus' in shorthand and '*3' in clean_harte_degrees:
                    clean_harte_degrees.remove('*3')
                break
        if shorthand:
            clean_harte_degrees = f'({",".join([x for x in clean_harte_degrees])})' if len(
                clean_harte_degrees) > 0 else ''
            if len(shorthand) > 0 or len(clean_harte_degrees) > 0:
                separator = ':'
            return self._root + separator + shorthand + clean_harte_degrees
        return self.chord

    def unwrap_shorthand(self) -> list[str] | None:
        """

        :return:
        """
        if self._shorthand:
            return self._all_degrees
        elif self._degrees:
            return self._degrees
        return None

    def __eq__(self, other):
        """

        :param other:
        :return:
        """
        if isinstance(other, Harte):
            return self._root == other.get_root() and self._degrees == \
                other.get_degrees() and self._bass == other.get_bass()
        return False

    def __repr__(self):
        """

        :return:
        """
        return f'Harte({self._root}:{self._shorthand}({self._degrees})/{self._bass})'

    def __str__(self):
        """

        :return:
        """
        return f'{self._root}:{self._shorthand}({self._degrees})/{self._bass}'


if __name__ == '__main__':
    # test utilities
    c = Harte('C:(3,5,7,9,11)/3')
    root = c.get_root()
    print(c.fullName)
    print(c.commonName)
    print(c.inversion())
    print(root, c.bass(), c.get_bass())
    print(c.prettify())
