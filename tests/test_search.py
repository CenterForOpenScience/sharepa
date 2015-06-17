from sharepa.search import ShareSearch
from sharepa.search import basic_search

import elasticsearch_dsl
import types


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


def test_execute():
    my_search = ShareSearch()

    result = my_search.execute()
    assert isinstance(result, elasticsearch_dsl.result.Response)


def test_count():
    count = basic_search.count()
    assert isinstance(count, int)


def test_query():
    assert isinstance(basic_search._query(basic_search.to_dict()), dict)


def test_scan():
    my_search = ShareSearch()
    my_search = my_search.query(
        'query_string',
        query='science AND cows AND milk'
    )

    scan = my_search.scan()
    scan_list = [item for item in scan]

    assert isinstance(scan, types.GeneratorType)
    assert scan_list
