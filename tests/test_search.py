import vcr
import elasticsearch_dsl

from sharepa.search import ShareSearch
from sharepa.search import basic_search
from .compat import text_type


@vcr.use_cassette('tests/vcr/basic_search_one.yaml')
def test_basic_search():
    results = basic_search.execute()
    assert results.hits
    assert results.aggregations


@vcr.use_cassette('tests/vcr/no_title_execute.yaml')
def test_no_title_search():
    my_search = ShareSearch()

    my_search = my_search.query(
        'query_string',
        query='NOT title:*',
        analyze_wildcard=True
    )
    results = my_search.execute()
    for result in results:
        assert result.title is None


@vcr.use_cassette('tests/vcr/simple_execute.yaml')
def test_execute():
    my_search = ShareSearch()
    result = my_search.execute()
    first_result = result.hits[0].to_dict()

    assert len(result.hits) == 10
    assert type(result) is elasticsearch_dsl.result.Response
    assert type(first_result['title']) is text_type


@vcr.use_cassette('tests/vcr/basic_search.yaml')
def test_count():
    count = basic_search.count()
    assert type(count) is int


def test_query():
    assert isinstance(basic_search._query(basic_search.to_dict()), dict)


@vcr.use_cassette('tests/vcr/scan.yaml')
def test_scan():
    my_search = ShareSearch()
    my_search = my_search.query(
        'query_string',
        query='squared'
    )
    scan = my_search.scan()
    scan_list = list(scan)
    assert type(scan_list[0].title) is text_type
