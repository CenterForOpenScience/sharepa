import vcr
import pandas
import pytest

from sharepa.search import ShareSearch
from sharepa.helpers import pretty_print
from sharepa.helpers import source_counts


@vcr.use_cassette('tests/vcr/simple_execute.yaml')
def test_pretty_print():
    my_search = ShareSearch()
    result = my_search.execute()
    the_dict = result.to_dict()
    try:
        pretty_print(the_dict)
    except:
        pytest.fail("Unexpected exception!!")


@vcr.use_cassette('tests/vcr/source_counts.yaml')
def test_source_counts():
    all_counts = source_counts()
    assert isinstance(all_counts, pandas.core.frame.DataFrame)
    assert all_counts.count().values[0] == 42
