"""
Map of the Harte shorthands available, mapped to their correspondent
chord tones/grades.
"""

from collections import OrderedDict

SHORTHAND_DEGREE_MAP = {
    'maj': ('3', '5'),
    'min': ('b3', '5'),
    'aug': ('3', '#5'),
    'dim': ('b3', 'b5'),
    'maj7': ('3', '5', '7'),
    'min7': ('b3', '5', 'b7'),
    '7': ('3', '5', 'b7'),
    'minmaj7': ('b3', '5', '7'),
    'dim7': ('b3', 'b5', 'bb7'),
    'hdim7': ('b3', 'b5', 'b7'),
    'maj6': ('3', '5', '6'),
    'min6': ('b3', '5', '6'),
    '9': ('3', '5', 'b7', '9'),
    'maj9': ('3', '5', '7', '9'),
    'min9': ('b3', '5', 'b7', '9'),
    'sus4': ('4', '5'),
}

DEGREE_SHORTHAND_MAP = OrderedDict({
    ('3', '5', 'b7', '9'): '9',
    ('3', '5', '7', '9'): 'maj9',
    ('b3', '5', 'b7', '9'): 'min9',
    ('3', '5', 'b7'): '7',
    ('3', '5', '6'): 'maj6',
    ('b3', '5', '6'): 'min6',
    ('3', '5', '7'): 'maj7',
    ('b3', 'b5', 'bb7'): 'dim7',
    ('b3', '5', 'b7'): 'min7',
    ('b3', 'b5', 'b7'): 'hdim7',
    ('b3', '5', '7'): 'minmaj7',
    ('3', '5'): 'maj',
    ('b3', '5'): 'min',
    ('b3', 'b5'): 'dim',
    ('3', '#5'): 'aug',
    ('4', '5'): 'sus4',
})
