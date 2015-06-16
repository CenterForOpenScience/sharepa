import pandas

from sharepa.helpers import pretty_print
from sharepa.helpers import source_counts


def test_pretty_print():
    some_stuff = '{"Dusty": "Rhodes"}'
    pretty_print(some_stuff)


def test_source_counts():
    all_counts = source_counts()
    assert isinstance(all_counts, pandas.core.frame.DataFrame)
