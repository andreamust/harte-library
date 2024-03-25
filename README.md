# The Harte Library

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://github.com/andreamust/harte-library/releases/)
[![PyPi version](https://badgen.net/pypi/v/pip/)](https://pypi.org/andreamust/harte-library)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)

The **Harte Library** is an extension of the [music21 library](http://web.mit.edu/music21/) tailored for working with music chords encoded according to the [Harte Notation](https://ismir2005.ismir.net/proceedings/1080.pdf).

This project is a component of [ChoCo](https://github.com/smashub/choco), a comprehensive dataset containing over 20,000 timed chord annotations sourced from integrated and standardized scores and tracks.

The library has the following dependencies:

- [music21](http://web.mit.edu/music21/): the base library the *harte-library* extends;
- [Lark](https://github.com/lark-parser/lark): for parsing the chords in Harte.

## 🛠️ Installation

The library is available on PyPi. To install, simply execute the following command:

```bash
pip install harte-library --upgrade
```

## 🔑 Key Features

The Harte Library offers several core functionalities:

- **Interoperability**: Seamlessly integrate musical chords notated in Harte Notation with the music21 library.
- **Interpretability**: Easily interpret chords notated in Harte format, including the unrolling of shorthand representations.
- **Simplification**: Streamline and standardize chords in Harte notation using the prettify_harte functionality.

## 🚀 Usage

### 🎵 Interval Module

The Harte Library extends the Interval Module of music21 to ensure interoperability between intervals expressed according to Harte notation and the interval class of music21.

The **HarteInterval** class accepts an interval expressed in Harte Notation as input and allows all the properties and methods of the music21 Interval module to be used:

```python
from harte.interval import HarteInterval

interval = HarteInterval('b6')

int_name = interval.name
int_is_consonant = interval.isConsonant()
```

### 🎸 Chord Module

The primary functionality of the Harte Library extends the Chord Module of music21.

This is achieved through the **Harte** class, which accepts a chord expressed in Harte Notation as input, enabling the utilization of all properties and methods available in the Chord module of music21:

```python
from harte.harte import Harte

chord = Harte('C#:maj7(b6)/b3')

bass = chord.bass()  # E
root = chord.root()  # C#
name = chord.fullName  # Chord {C-sharp in octave 4 | E in octave 3 | E-sharp in octave 4 | G-sharp in octave 4 | A in octave 4 | B-sharp in octave 4} Quarter
```

Additionally, the library introduces new methods tailored specifically for Harte notation, including:

- **get_degrees()**: Retrieves the intervals of the chord, excluding those represented by shorthand.
- **get_midi_pitches()**: Obtains the MIDI pitches of the chord as an ordered list.
- **get_root()**: Retrieves the root of the chord as a string.
- **get_bass()**: Calculates the interval between the root note and the bass note.
- **contains_shorthand()**: Determines whether the chord contains a shorthand representation, returning `True` if present, `False` otherwise.
- **get_shorthand()**: Retrieves the shorthand representation of the chord, if available.
- **unwrap_shorthand()**: Unwraps the shorthand notation, returning a list containing all intervals in the chord, including those represented by shorthand.
- **prettify()**: Decomposes the chord into its constituent components and recomposes it by selecting the most concise shorthand representation, if applicable.

```python
from harte.harte import Harte

chord = Harte('D:(b3,5,7,9)')

pretty_harte = chord.prettify()  # D:minmaj7(9)
```

## 🤝 Contributing

We welcome contributions from the community to enhance the Harte Library. Whether you want to report a bug, suggest a new feature, or contribute code, your help is greatly appreciated!

## 🐞 Reporting Issues

If you encounter any bugs, have feature requests, or have suggestions for improvements, please open an [issue](https://github.com/andreamust/harte-library/issues) with detailed information about the problem or suggestion.

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
