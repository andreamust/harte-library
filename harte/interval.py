"""
Extension of the Interval class from music21.interval to support the
Harte notation.
"""

from music21.interval import Interval, IntervalException
from music21.note import Note

from harte.utils import convert_interval


class HarteInterval(Interval):
    """
    music21 Interval class extension to support the Harte notation.
    """

    def __init__(self, harte_interval: str, **keywords) -> None:
        """
        Constructor for the HarteInterval class. It takes a string containing
        an interval as expressed by the Harte notation (e.g. 'b2') and aligns
        it to the music21 notation (e.g. 'm2'), by initializing the parent
        constructor
        :param harte_interval: A string containing an interval as expressed
        by the Harte notation (e.g. 'b2')
        :type harte_interval: str
        """
        self._harte_interval = harte_interval
        try:
            self._converted_interval = convert_interval(self._harte_interval)
        except ValueError as value_error:
            raise IntervalException(
                'Harte Interval cannot be converted') from value_error
        self._converted_interval = convert_interval(self._harte_interval)
        super().__init__(self._converted_interval, **keywords)

    def __eq__(self, other) -> bool:
        """
        Defines the equality operator for the HarteInterval class
        :param other: The other HarteInterval object to compare to
        :type other: HarteInterval
        :return: True if the two HarteInterval objects are equal, False
        otherwise.
        """
        if isinstance(other, HarteInterval):
            return self._harte_interval == other._harte_interval
        return self._harte_interval == other

    def __repr__(self) -> str:
        """
        Returns a string representation of the HarteInterval object
        :return: A string representation of the HarteInterval object
        """
        return f'HarteInterval({self._harte_interval})'

    def __str__(self) -> str:
        """
        Returns a string representation of the HarteInterval object
        :return: A string representation of the HarteInterval object
        """
        return self._harte_interval


if __name__ == '__main__':
    i = HarteInterval('3').transposeNote(Note('C'))
    print(i)
