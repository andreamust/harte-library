# The Harte Library

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://github.com/andreamust/harte-library/releases/)
[![PyPi version](https://badgen.net/pypi/v/pip/)](https://pypi.org/andreamust/harte-library)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)


Extension of the [music21 library](http://web.mit.edu/music21/) for working with music chords encoded according to the [Harte Notation](https://ismir2005.ismir.net/proceedings/1080.pdf).

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


### Chord Module Extension



Ideas:
* harte_simplifier
* harte extender (from shortcut to extended)
* harte to pitch class
* ???

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

