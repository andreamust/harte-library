"""

"""

from music21.chord import Chord, ChordException
from music21.pitch import Pitch

from parse_harte import PARSER
from harte_utils import convert_interval


class Harte(Chord):
    """

    """
    def __init__(self, chord: str, **keywords):
        """

        :param chord:
        :type chord: str
        """
        try:
            parsed_chord = PARSER.parse(chord)
            print(parsed_chord)
        except NameError:
            raise ChordException(
                f'The input chord {chord} is not a valid Harte chord')

        assert parsed_chord['root']

        self._root = parsed_chord['root']
        self._shorthand = parsed_chord[
            'shorthand'] if 'shorthand' in parsed_chord.keys() else None
        self._degrees = parsed_chord[
            'degrees'] if 'degrees' in parsed_chord.keys() else None
        self._bass = parsed_chord[
            'bass'] if 'bass' in parsed_chord.keys() else None

        self.Chord = Chord([Pitch(self._bass, octave=4)])
        print(self.Chord)

        super().__init__(**keywords)

    def get_degrees(self) -> list[str]:
        """

        :return:
        """
        pass

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

    def simplify(self) -> str:
        """

        :return:
        """
        pass

    def unwrap_shorthand(self) -> str:
        """

        :return:
        """
        pass

    def __repr__(self):
        """

        :return:
        """
        pass

    def __str__(self):
        """

        :return:
        """
        pass


if __name__ == '__main__':
    # test utilities
    c = Harte('C:(3,5,6)')
    root = c.get_root()
    print(root)
