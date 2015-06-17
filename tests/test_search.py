import vcr
import elasticsearch_dsl

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


@vcr.use_cassette('tests/vcr/simple_execute.yaml')
def test_execute():
    my_search = ShareSearch()
    result = my_search.execute()
    first_result = result.hits[0].to_dict()

    assert len(result.hits) == 10
    assert result.to_dict().keys() == ['hits', '_shards', 'took', 'timed_out', 'time']
    assert isinstance(result, elasticsearch_dsl.result.Response)
    assert first_result['title'] == 'Avian community structure and incidence of human West Nile infection'


def test_count():
    count = basic_search.count()
    assert isinstance(count, int)


def test_query():
    assert isinstance(basic_search._query(basic_search.to_dict()), dict)


@vcr.use_cassette('tests/vcr/scan.yaml')
def test_scan():
    my_search = ShareSearch()
    my_search = my_search.query(
        'query_string',
        query='squared AND circle'
    )
    scan = my_search.scan()
    scan_list = [item for item in scan]
    assert len(scan_list) == 3
    assert scan_list[0].title == '<p>The ellipsoids in the figure are isolines of constant density of bivariate Gaussian distributions.</p>'
