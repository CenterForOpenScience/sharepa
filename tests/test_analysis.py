from sharepa.analysis import agg_to_two_dim_dataframe, merge_dataframes, bucket_to_dataframe
from sharepa.search import ShareSearch
from elasticsearch_dsl.utils import AttrDict
import pandas as pd
from mock import Mock
from sharepa.analysis import agg_to_two_dim_dataframe
import pytest

def test_bucket_to_data_frame():
    search_basic = ShareSearch()
    search_basic.aggs.bucket(
        'agg_by_subs',  # Every aggregation needs a name
        'terms',
        field='subjects',
        size=10,
        min_doc_count=0
    )

    # Create Mock object for test so we are not actually hitting server:
    search_mock = AttrDict({u'agg_by_subs':
        {u'buckets':
            [
                {u'key': u'and', u'doc_count': 90372},
                {u'key': u'article', u'doc_count': 81837},
                {u'key': u'physics', u'doc_count': 74792},
                {u'key': u'astrophysics', u'doc_count': 45266},
                {u'key': u'energy', u'doc_count': 41402},
                {u'key': u'high', u'doc_count': 41272},
                {u'key': u'mathematics', u'doc_count': 37734},
                {u'key': u'research', u'doc_count': 36819},
                {u'key': u'theory', u'doc_count': 34277},
                {u'key': u'matter', u'doc_count': 33688}
            ]
        }
    })
    search_basic.execute = Mock(return_value=search_mock)
    search_results = search_basic.execute()
    basic_dataframe = bucket_to_dataframe('ten_top_subjects', search_results.agg_by_subs.buckets)
    assert isinstance(basic_dataframe, pd.DataFrame)
    assert basic_dataframe.shape[0] == 10
    for index, row_count in enumerate(basic_dataframe.ten_top_subjects):
        assert row_count == search_results.agg_by_subs.buckets[index].ten_top_subjects
    for index, row_name in enumerate(basic_dataframe.key):
        assert row_name == search_results.agg_by_subs.buckets[index].key

def test_basic_aggregation():
    search_with_basic_aggs = ShareSearch()
    search_with_basic_aggs.aggs.bucket(
        'testing_basic_agg',  # Every aggregation needs a name
        'terms',
        field='subjects',
        size=10,
        min_doc_count=0
    )

    # Create Mock object for test so we are not actually hitting server:
    search_mock = AttrDict({u'testing_basic_agg':
        {u'buckets':
            [
                {u'key': u'and', u'doc_count': 90372},
                {u'key': u'article', u'doc_count': 81837},
                {u'key': u'physics', u'doc_count': 74792},
                {u'key': u'astrophysics', u'doc_count': 45266},
                {u'key': u'energy', u'doc_count': 41402},
                {u'key': u'high', u'doc_count': 41272},
                {u'key': u'mathematics', u'doc_count': 37734},
                {u'key': u'research', u'doc_count': 36819},
                {u'key': u'theory', u'doc_count': 34277},
                {u'key': u'matter', u'doc_count': 33688}
            ]
        }
    })
    search_with_basic_aggs.execute = Mock(return_value=search_mock)
    search_results = search_with_basic_aggs.execute()
    basic_dataframe = agg_to_two_dim_dataframe(search_results.testing_basic_agg)
    assert isinstance(basic_dataframe, pd.DataFrame)
    assert basic_dataframe.shape[0] == 10
    for index, row_count in enumerate(basic_dataframe.doc_count):
        assert row_count == search_results.testing_basic_agg.buckets[index].doc_count
    for index, row_name in enumerate(basic_dataframe.key):
        assert row_name == search_results.testing_basic_agg.buckets[index].key



def test_two_dim_aggregation():
    num_cols = 5
    search_with_two_dim_aggs = ShareSearch()
    search_with_two_dim_aggs.aggs.bucket(
        'testing_two_dim_agg',
        'terms',
        field='subjects',
        size=num_cols,
        min_doc_count=0
    ).metric(
        'dates',
        'date_histogram',
        field='providerUpdatedDateTime',
        interval='1M',
        format='yyyy-MM-dd',
        extended_bounds={
            "min": "2014-01-01",
            "max": "2014-12-31"},
        min_doc_count=0
    )

    # Create Mock object for test so we are not actually hitting server:
    search_mock = AttrDict({u'testing_two_dim_aggs':
                                {u'buckets':
                                     [{u'dates': {u'buckets':
                                                      [{u'key': 1388534400000, u'key_as_string': u'2014-01-01',
                                                        u'doc_count': 0},
                                                       {u'key': 1391212800000, u'key_as_string': u'2014-02-01',
                                                        u'doc_count': 0},
                                                       {u'key': 1393632000000, u'key_as_string': u'2014-03-01',
                                                        u'doc_count': 0},
                                                       {u'key': 1396310400000, u'key_as_string': u'2014-04-01',
                                                        u'doc_count': 0},
                                                       {u'key': 1398902400000, u'key_as_string': u'2014-05-01',
                                                        u'doc_count': 0},
                                                       {u'key': 1401580800000, u'key_as_string': u'2014-06-01',
                                                        u'doc_count': 0},
                                                       {u'key': 1404172800000, u'key_as_string': u'2014-07-01',
                                                        u'doc_count': 0},
                                                       {u'key': 1406851200000, u'key_as_string': u'2014-08-01',
                                                        u'doc_count': 0},
                                                       {u'key': 1409529600000, u'key_as_string': u'2014-09-01',
                                                        u'doc_count': 0},
                                                       {u'key': 1412121600000, u'key_as_string': u'2014-10-01',
                                                        u'doc_count': 4286},
                                                       {u'key': 1414800000000, u'key_as_string': u'2014-11-01',
                                                        u'doc_count': 7415},
                                                       {u'key': 1417392000000, u'key_as_string': u'2014-12-01',
                                                        u'doc_count': 4732},
                                                       {u'key': 1420070400000, u'key_as_string': u'2015-01-01',
                                                        u'doc_count': 4623},
                                                       {u'key': 1422748800000, u'key_as_string': u'2015-02-01',
                                                        u'doc_count': 8219},
                                                       {u'key': 1425168000000, u'key_as_string': u'2015-03-01',
                                                        u'doc_count': 10152},
                                                       {u'key': 1427846400000, u'key_as_string': u'2015-04-01',
                                                        u'doc_count': 10658},
                                                       {u'key': 1430438400000, u'key_as_string': u'2015-05-01',
                                                        u'doc_count': 22954},
                                                       {u'key': 1433116800000, u'key_as_string': u'2015-06-01',
                                                        u'doc_count': 17333}]},
                                       u'key': u'and', u'doc_count': 90372},
                                      {u'dates': {u'buckets':
                                                      [{u'key': 1388534400000, u'doc_count': 0,
                                                        u'key_as_string': u'2014-01-01'},
                                                       {u'key': 1391212800000, u'doc_count': 0,
                                                        u'key_as_string': u'2014-02-01'},
                                                       {u'key': 1393632000000, u'doc_count': 0,
                                                        u'key_as_string': u'2014-03-01'},
                                                       {u'key': 1396310400000, u'doc_count': 0,
                                                        u'key_as_string': u'2014-04-01'},
                                                       {u'key': 1398902400000, u'doc_count': 0,
                                                        u'key_as_string': u'2014-05-01'},
                                                       {u'key': 1401580800000, u'doc_count': 0,
                                                        u'key_as_string': u'2014-06-01'},
                                                       {u'key': 1404172800000, u'doc_count': 0,
                                                        u'key_as_string': u'2014-07-01'},
                                                       {u'key': 1406851200000, u'doc_count': 0,
                                                        u'key_as_string': u'2014-08-01'},
                                                       {u'key': 1409529600000, u'doc_count': 0,
                                                        u'key_as_string': u'2014-09-01'},
                                                       {u'key': 1412121600000, u'doc_count': 0,
                                                        u'key_as_string': u'2014-10-01'},
                                                       {u'key': 1414800000000, u'doc_count': 0,
                                                        u'key_as_string': u'2014-11-01'},
                                                       {u'key': 1417392000000, u'doc_count': 1685,
                                                        u'key_as_string': u'2014-12-01'},
                                                       {u'key': 1420070400000, u'doc_count': 13871,
                                                        u'key_as_string': u'2015-01-01'},
                                                       {u'key': 1422748800000, u'doc_count': 10175,
                                                        u'key_as_string': u'2015-02-01'},
                                                       {u'key': 1425168000000, u'doc_count': 14745,
                                                        u'key_as_string': u'2015-03-01'},
                                                       {u'key': 1427846400000, u'doc_count': 13881,
                                                        u'key_as_string': u'2015-04-01'},
                                                       {u'key': 1430438400000, u'doc_count': 16696,
                                                        u'key_as_string': u'2015-05-01'},
                                                       {u'key': 1433116800000, u'doc_count': 10784,
                                                        u'key_as_string': u'2015-06-01'}]},
                                       u'key': u'article', u'doc_count': 81837}]
                                 }})

    search_with_two_dim_aggs.execute = Mock(return_value=search_mock)
    search_results = search_with_two_dim_aggs.execute()
    two_dim_dataframe = agg_to_two_dim_dataframe(search_results.testing_two_dim_aggs)
    assert isinstance(two_dim_dataframe, pd.DataFrame)
    assert two_dim_dataframe.shape[1] == 4
    assert two_dim_dataframe.shape[0] == 18
    for index, bucket in enumerate(search_results.testing_two_dim_aggs.buckets):
        for index_2nd_level, raw_date in enumerate(two_dim_dataframe['dates.key']):
            assert raw_date == search_results.testing_two_dim_aggs.buckets[index].dates.buckets[index_2nd_level][
                'dates.key']
    for index_2nd_level, count_num in enumerate(two_dim_dataframe['dates.and']):
        assert count_num == search_results.testing_two_dim_aggs.buckets[0].dates.buckets[index_2nd_level]['dates.and']


def test_throw_error_in_agg_convert_when_too_many_levels():
    num_cols = 5
    search_with_multilevel = ShareSearch()
    search_with_multilevel.aggs.bucket(
        'testing_two_dim_agg',
        'terms',
        field='subjects',
        size=num_cols,
        min_doc_count=0
    ).metric(
        'source',
        'terms',
        field='source',
        size=10,
        min_doc_count=0
    ).metric(
        'dates',
        'date_histogram',
        field='providerUpdatedDateTime',
        interval='1M',
        format='yyyy-MM-dd',
        extended_bounds={
            "min": "2014-01-01",
            "max": "2014-12-31"},
        min_doc_count=0
    )

    # Create Mock object for test so we are not actually hitting server:
    search_mock = AttrDict({u'testing_multilevel':
        {u'buckets':
            [
                {
                    u"source": {u"buckets":
                                    [{u"key": u"dataone", u"doc_count": 15760},
                                     {u"key": u"clinicaltrials", u"doc_count": 21}]
                                },
                    u'dates': {u'buckets':
                                   [{u'key': 1388534400000, u'key_as_string': u'2014-01-01', u'doc_count': 0},
                                    {u'key': 1391212800000, u'key_as_string': u'2014-02-01', u'doc_count': 0},
                                    {u'key': 1393632000000, u'key_as_string': u'2014-03-01', u'doc_count': 0},
                                    {u'key': 1396310400000, u'key_as_string': u'2014-04-01', u'doc_count': 0},
                                    {u'key': 1398902400000, u'key_as_string': u'2014-05-01', u'doc_count': 0},
                                    {u'key': 1401580800000, u'key_as_string': u'2014-06-01', u'doc_count': 0},
                                    {u'key': 1404172800000, u'key_as_string': u'2014-07-01', u'doc_count': 0},
                                    {u'key': 1406851200000, u'key_as_string': u'2014-08-01', u'doc_count': 0},
                                    {u'key': 1409529600000, u'key_as_string': u'2014-09-01', u'doc_count': 0},
                                    {u'key': 1412121600000, u'key_as_string': u'2014-10-01', u'doc_count': 4286},
                                    {u'key': 1414800000000, u'key_as_string': u'2014-11-01', u'doc_count': 7415},
                                    {u'key': 1417392000000, u'key_as_string': u'2014-12-01', u'doc_count': 4732},
                                    {u'key': 1420070400000, u'key_as_string': u'2015-01-01', u'doc_count': 4623},
                                    {u'key': 1422748800000, u'key_as_string': u'2015-02-01', u'doc_count': 8219},
                                    {u'key': 1425168000000, u'key_as_string': u'2015-03-01', u'doc_count': 10152},
                                    {u'key': 1427846400000, u'key_as_string': u'2015-04-01', u'doc_count': 10658},
                                    {u'key': 1430438400000, u'key_as_string': u'2015-05-01', u'doc_count': 22954},
                                    {u'key': 1433116800000, u'key_as_string': u'2015-06-01', u'doc_count': 17333}]
                               },
                    u'key': u'and', u'doc_count': 90372
                },
                {
                    u"source":{u"buckets":
                        [
                            {u"key": u"dataone", u"doc_count": 100},
                            {u"key": u"clinicaltrials", u"doc_count": 4}
                        ]
                    },
                    u'dates': {u'buckets':
                                [{u'key': 1388534400000, u'doc_count': 0, u'key_as_string': u'2014-01-01'},
                                 {u'key': 1391212800000, u'doc_count': 0, u'key_as_string': u'2014-02-01'},
                                 {u'key': 1393632000000, u'doc_count': 0, u'key_as_string': u'2014-03-01'},
                                 {u'key': 1396310400000, u'doc_count': 0, u'key_as_string': u'2014-04-01'},
                                 {u'key': 1398902400000, u'doc_count': 0, u'key_as_string': u'2014-05-01'},
                                 {u'key': 1401580800000, u'doc_count': 0, u'key_as_string': u'2014-06-01'},
                                 {u'key': 1404172800000, u'doc_count': 0, u'key_as_string': u'2014-07-01'},
                                 {u'key': 1406851200000, u'doc_count': 0, u'key_as_string': u'2014-08-01'},
                                 {u'key': 1409529600000, u'doc_count': 0, u'key_as_string': u'2014-09-01'},
                                 {u'key': 1412121600000, u'doc_count': 0, u'key_as_string': u'2014-10-01'},
                                 {u'key': 1414800000000, u'doc_count': 0, u'key_as_string': u'2014-11-01'},
                                 {u'key': 1417392000000, u'doc_count': 1685, u'key_as_string': u'2014-12-01'},
                                 {u'key': 1420070400000, u'doc_count': 13871, u'key_as_string': u'2015-01-01'},
                                 {u'key': 1422748800000, u'doc_count': 10175, u'key_as_string': u'2015-02-01'},
                                 {u'key': 1425168000000, u'doc_count': 14745, u'key_as_string': u'2015-03-01'},
                                 {u'key': 1427846400000, u'doc_count': 13881, u'key_as_string': u'2015-04-01'},
                                 {u'key': 1430438400000, u'doc_count': 16696, u'key_as_string': u'2015-05-01'},
                                 {u'key': 1433116800000, u'doc_count': 10784, u'key_as_string': u'2015-06-01'}]},
                 u'key': u'article', u'doc_count': 81837
                }
            ]
        }
    })

    search_with_multilevel.execute = Mock(return_value=search_mock)
    search_results = search_with_multilevel.execute()
    with pytest.raises(ValueError):
        multilevel_dataframe = agg_to_two_dim_dataframe(search_results.testing_multilevel)

def test_merge_dataframes():
    dream = pd.DataFrame({'Rhodes': 'Dusty'}, index=['Rhodes'])
    stardust = pd.DataFrame({'Rhodes': 'Cody'}, index=['Rhodes'])

    family = merge_dataframes(dream, stardust)

    assert isinstance(family, pd.core.frame.DataFrame)
    assert family.columns.values.tolist() == ['Rhodes', 'Rhodes']
    assert family.index.item() == 'Rhodes'
