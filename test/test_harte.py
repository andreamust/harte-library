import os
import json
import pytest
from harte.harte import Harte

# load a dict of chords frequencies extracted from ChoCo [1] 
# to test coverage of a big set of chords
# [1] https://github.com/smashub/choco
CUR_DIR = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(CUR_DIR, "chords_count.json")) as f:
  CHORDS_COUNT = json.load(f)

@pytest.mark.parametrize("chord", list(CHORDS_COUNT.keys()))
def test_coverage(chord: str):
  """
  Tests coverage of all chord extracted from ChoCo [1].

  [1] https://github.com/smashub/choco

  :param chord: Chord to be tested
  :type chord: str
  """
  assert Harte(chord)
