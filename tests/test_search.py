from sharepa.search import ShareSearch
from sharepa.search import basic_search


def test_basic_search():
    results = basic_search.execute()
    assert results.hits
    assert results.aggregations


def test_no_title_search():
    my_search = ShareSearch()

    my_search = my_search.query(
        'query_string',
        query='NOT title:*',
        analyze_wildcard=True
    )
    results = my_search.execute()
    for result in results:
        assert not result.get('title')
