# The Harte Library

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://github.com/andreamust/harte-library/releases/)
[![PyPi version](https://badgen.net/pypi/v/pip/)](https://pypi.org/andreamust/harte-library)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)


Extension of the [music21 library](http://web.mit.edu/music21/) for working with music chords encoded according to the [Harte Notation](https://ismir2005.ismir.net/proceedings/1080.pdf).

This project is part of [ChoCo](https://github.com/smashub/choco), a dataset of 20K+ timed chord annotations of integrated and standardised scores and tracks.

The Harte Library mainly extends the *Chord module* of muisc21. In addition, the *Interval module* is also extended to support intervals as represented in the chords encoded in Harte.

The library has the following dependencies:
- [music21](http://web.mit.edu/music21/): as an extension of the library itself;
- [Lark](https://github.com/lark-parser/lark): for parsing the chords in Harte.

## Installation

The library has been uploaded to PyPi, therefore for installation simply launch:

```bash
pip install harte-library
```

## Main Functionalities

The main functionalities of the Harte Library are:

* to make musical chords notated according to Harte Notation interoperable with the music21 library;
* to make chords notated in Harte interpretable, e.g. by unrolling the shorthand;
* to simplify and homogenise chords in Harte, via the *prettify_harte* functionality.

## Usage

### Interval Module Extension

The Harte Library extends the *Interval Module* of music21 to ensure interoperability between intervals expressed according to Harte notation and the interval class of music21.

The __HarteInterval__ class accepts an interval expressed in Harte Notation as input and allows all the properties and methods of the music21 Interval module to be used:

```python
from harte.interval import HarteInterval

interval = HarteInterval('b6')

int_name = interval.name
int_is_consonant = interval.isConsonant()
```

### Chord Module Extension

The main functionality of the Harte Library is an extension of the *Chord Module* of music21.

This is possible by means of the class __Harte__, which accepts as input a chord expressed in Harte Notation and allows all properties and methods of the Chord module of music21 to be used:

```python
from harte.harte import Harte

chord = Harte('C#:maj7(b6)/b3')

bass = chord.bass()  # E
root = chord.root()  # C#
name = chord.fullName  # Chord {G-sharp | A | E | B-sharp | C-sharp | E-sharp} Quarter
```

In addition, the library implements new methods specific to Harte notation, including:
* __get_degrees__: returns the intervals of the chord, disregarding those expressed by the shorthand
* __get_root__: returns the root of the chord expressed as a string
* __get_bass__: returns the interval between the root note and the bass note
* __contains_shorthand__: returns `True` if the chord contains a shorthand, `False` otherwise
* __get_shorthand__: returns the chord's shorthand, if present
* __unwrap_shorthand__: returns a list containing all the intervals in the chord, including those wrapped by the shorthand
* __prettify__: breaks the chord into its components and recomposes it by choosing the most summarised shorthand, if possible.

```python
from harte.harte import Harte

chord = Harte('D:(b3,5,7,9)')

pretty_harte = chord.prettify()  # D:minmaj7(9)
```

## Contributing

Every type of contribution to the library is widely encouraged.
The library has also just been released and any bug reports are highly appreciated.

## License

MIT License

Copyright (c) 2022 Andrea Poltronieri

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

