"""

"""

from music21.interval import Interval

import re

class HarteInterval(Interval):
    """


    """
    def __init__(self, harte_interval: str, **keywords):
        """

        :param harte_interval:
        :type interval: str
        """
        self._harte_interval = harte_interval

        super().__init__(**keywords)


    def _convert_interval(self):
        """

        """
        regex = r'([#]+)?([b]+)?(\d+)'
        # find all matches
        matches = re.findall(regex, self._harte_interval)[0]
        if int(matches[2]) in [1,4,5]:

        print(matches)


if __name__ == '__main__':
    interval = HarteInterval('13')
    interval._convert_interval()

