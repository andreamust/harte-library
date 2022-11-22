"""

"""


class Hartify:
    """

    """
    def __init__(self, harte_chord: str) -> None:
        """

        :param harte_chord:
        """
        if type(harte_chord) != str or ':' not in harte_chord:
            raise ValueError('The given chord is not a valid Harte Chord.')
        self.harte_chord = harte_chord

    def __del__(self):
        """

        :return:
        """
        print('Not a valid Harte Chord.')

    def decode(self):
        """

        :return:
        """
        pass

    def encode(self):
        """

        :return:
        """
        pass

Hartify(0)