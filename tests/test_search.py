from sharepa.search import basic_search


def test_basic_search():
    results = basic_search.execute()
    assert results.hits
    assert results.aggregations
