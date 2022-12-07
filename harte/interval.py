"""

"""

from music21.interval import Interval, IntervalException

from utils import convert_interval


class HarteInterval(Interval):
    """

    """

    def __init__(self, harte_interval: str):
        """

        :param harte_interval:
        :type harte_interval: str
        """
        self._harte_interval = harte_interval
        try:
            self._converted_interval = convert_interval(self._harte_interval)
        except ValueError:
            raise IntervalException('Harte Interval cannot be converted')
        super().__init__(convert_interval(self._harte_interval))

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
    interval = HarteInterval('bb3').name
    print(interval)
