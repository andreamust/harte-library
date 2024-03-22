"""
Exceptions for the harte package.
"""
from music21.chord import ChordException


class ChordEmptyError(ChordException):
    """
    Exception raised when a chord is empty.
    """

    def __init__(self, chord):
        """
        Constructor for the ChordEmptyError class.
        :param chord: The chord that is empty.
        :type chord: Chord
        """
        self.chord = chord
        self.message = f"The chord {self.chord} is empty."
        super().__init__(self.message)
