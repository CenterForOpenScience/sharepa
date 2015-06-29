import json
import sys
from sharepa.search import ShareSearch
from sharepa.experimental_analysis_functions import convert_nested_to_dataframe
from elasticsearch_dsl.utils import AttrDict
from mock import Mock



def pretty_print(d):
    print(json.dumps(d, indent=4))

def test_convert_nested_to_dataframe_crossed():
    my_search = ShareSearch()  # BASE_URL='https://staging.osf.io/api/v1/share/search/')

    # first we test crossed data
    my_search.aggs.bucket(
        'tags',  # Every aggregation needs a name
        'terms',
        field='tags',
        # We store the source of a document in its type, so this will aggregate by source #BYNOTE so this looks at the type feild and agregates by that?
        size=3,  # These are just to make sure we get numbers for all the sources, to make it easier to combine graphs
        min_doc_count=0,
    ).metric(
        'source',
        'terms',
        field='source',
        size=3,
        min_doc_count=0
    ).metric(
        'dates',
        'date_histogram',
        field='providerUpdatedDateTime',
        interval='1y',
        format='yyyy-MM-dd',
        extended_bounds={
            "min": "2014-01-01",
            "max": "2015-01-01"},
        min_doc_count=0
    )

    search_mock = AttrDict({u'aggregations':{u'tags': {u'buckets':
                                          [{u'dates': {u'buckets': [{u'doc_count': 5,
                                                                     u'key': 1388534400000,
                                                                     u'key_as_string': u'2014-01-01'},
                                                                    {u'doc_count': 15776,
                                                                     u'key': 1420070400000,
                                                                     u'key_as_string': u'2015-01-01'}]},
                                            u'doc_count': 15781,
                                            u'key': u'water',
                                            u'source': {u'buckets': [{u'doc_count': 15760, u'key': u'dataone'},
                                                                     {u'doc_count': 21, u'key': u'clinicaltrials'},
                                                                     {u'doc_count': 0, u'key': u'arxiv_oai'}],
                                                        u'doc_count_error_upper_bound': 0,
                                                        u'sum_other_doc_count': 0}},
                                           {u'dates': {u'buckets': [{u'doc_count': 0,
                                                                     u'key': 1388534400000,
                                                                     u'key_as_string': u'2014-01-01'},
                                                                    {u'doc_count': 15505,
                                                                     u'key': 1420070400000,
                                                                     u'key_as_string': u'2015-01-01'}]},
                                            u'doc_count': 15505,
                                            u'key': u'california',
                                            u'source': {u'buckets': [{u'doc_count': 15505, u'key': u'dataone'},
                                                                     {u'doc_count': 0, u'key': u'arxiv_oai'},
                                                                     {u'doc_count': 0, u'key': u'asu'}],
                                                        u'doc_count_error_upper_bound': 0,
                                                        u'sum_other_doc_count': 0}},
                                           {u'dates': {u'buckets': [{u'doc_count': 1,
                                                                     u'key': 1388534400000,
                                                                     u'key_as_string': u'2014-01-01'},
                                                                    {u'doc_count': 14825,
                                                                     u'key': 1420070400000,
                                                                     u'key_as_string': u'2015-01-01'}]},
                                            u'doc_count': 14826,
                                            u'key': u'county',
                                            u'source': {u'buckets': [{u'doc_count': 14825, u'key': u'dataone'},
                                                                     {u'doc_count': 1, u'key': u'clinicaltrials'},
                                                                     {u'doc_count': 0, u'key': u'arxiv_oai'}],
                                                        u'doc_count_error_upper_bound': 0,
                                                        u'sum_other_doc_count': 0}}],
                                      u'doc_count_error_upper_bound': 5860,
                                      u'sum_other_doc_count': 706643}}})

    my_search.execute = Mock(return_value=search_mock)
    my_results = my_search.execute()
    my_dataframe = convert_nested_to_dataframe(my_results.aggregations)

    assert my_dataframe.shape == (9, 5)
    for tag_buckets in my_results.aggregations.tags.buckets:
        assert tag_buckets.key in my_dataframe['tags'].values.tolist()
        for source_buckets in tag_buckets.source.buckets:
            assert source_buckets.source in my_dataframe['source'].values.tolist() or (dates_buckets.dates is 'NaN')
        for dates_buckets in tag_buckets.dates.buckets:
            assert (dates_buckets.dates in my_dataframe['dates'].values.tolist()) or (dates_buckets.dates is 'NaN')

def test_convert_nested_to_dataframe_nested():
    my_search = ShareSearch()
    my_search.aggs.bucket(
      'tags',  # Every aggregation needs a name
      'terms',
      field='tags',
      # We store the source of a document in its type, so this will aggregate by source #BYNOTE so this looks at the type feild and agregates by that?
      size=3,  # These are just to make sure we get numbers for all the sources, to make it easier to combine graphs
      min_doc_count=0,
    ).bucket(
      'source',
      'terms',
      field='source',
      size=3,
      min_doc_count=0
    ).bucket(
      'dates',
      'date_histogram',
      field='providerUpdatedDateTime',
      interval='1y',
      format='yyyy-MM-dd',
      extended_bounds={
         "min": "2014-11-01",
         "max": "2015-01-01"},
      min_doc_count=0
    )

    search_mock = AttrDict({u'aggregations':
      {u'tags': {u'buckets': [{u'doc_count': 15781,
                               u'key': u'water',
                               u'source': {u'buckets': [
                                  {u'dates': {u'buckets':
                                                 [{u'doc_count': 0,
                                                   u'key': 1388534400000,
                                                   u'key_as_string': u'2014-01-01'},
                                                  {u'doc_count': 15760,
                                                   u'key': 1420070400000,
                                                   u'key_as_string': u'2015-01-01'}
                                                  ]},
                                   u'doc_count': 15760,
                                   u'key': u'dataone'},
                                  {u'dates': {u'buckets':
                                                 [{u'doc_count': 5,
                                                   u'key': 1388534400000,
                                                   u'key_as_string': u'2014-01-01'},
                                                  {u'doc_count': 16,
                                                   u'key': 1420070400000,
                                                   u'key_as_string': u'2015-01-01'}
                                                  ]},
                                   u'doc_count': 21,
                                   u'key': u'clinicaltrials'},
                                  {u'dates': {u'buckets':
                                                 [{u'doc_count': 0,
                                                   u'key': 1388534400000,
                                                   u'key_as_string': u'2014-01-01'},
                                                  {u'doc_count': 0,
                                                   u'key': 1420070400000,
                                                   u'key_as_string': u'2015-01-01'}
                                                  ]},
                                   u'doc_count': 0,
                                   u'key': u'arxiv_oai'}],
                                  u'doc_count_error_upper_bound': 0,
                                  u'sum_other_doc_count': 0}},
                              {u'doc_count': 15505,
                               u'key': u'california',
                               u'source': {u'buckets': [{u'dates': {u'buckets': [{u'doc_count': 0,
                                                                                  u'key': 1388534400000,
                                                                                  u'key_as_string': u'2014-01-01'},
                                                                                 {u'doc_count': 15505,
                                                                                  u'key': 1420070400000,
                                                                                  u'key_as_string': u'2015-01-01'}]},
                                                         u'doc_count': 15505,
                                                         u'key': u'dataone'},
                                                        {u'dates': {u'buckets': [{u'doc_count': 0,
                                                                                  u'key': 1388534400000,
                                                                                  u'key_as_string': u'2014-01-01'},
                                                                                 {u'doc_count': 0,
                                                                                  u'key': 1420070400000,
                                                                                  u'key_as_string': u'2015-01-01'}]},
                                                         u'doc_count': 0,
                                                         u'key': u'arxiv_oai'},
                                                        {u'dates': {u'buckets': [{u'doc_count': 0,
                                                                                  u'key': 1388534400000,
                                                                                  u'key_as_string': u'2014-01-01'},
                                                                                 {u'doc_count': 0,
                                                                                  u'key': 1420070400000,
                                                                                  u'key_as_string': u'2015-01-01'}]},
                                                         u'doc_count': 0,
                                                         u'key': u'asu'}],
                                           u'doc_count_error_upper_bound': 0,
                                           u'sum_other_doc_count': 0}},
                              {u'doc_count': 14826,
                               u'key': u'county',
                               u'source': {u'buckets': [{u'dates': {u'buckets': [{u'doc_count': 0,
                                                                                  u'key': 1388534400000,
                                                                                  u'key_as_string': u'2014-01-01'},
                                                                                 {u'doc_count': 14825,
                                                                                  u'key': 1420070400000,
                                                                                  u'key_as_string': u'2015-01-01'}]},
                                                         u'doc_count': 14825,
                                                         u'key': u'dataone'},
                                                        {u'dates': {u'buckets': [{u'doc_count': 1,
                                                                                  u'key': 1388534400000,
                                                                                  u'key_as_string': u'2014-01-01'},
                                                                                 {u'doc_count': 0,
                                                                                  u'key': 1420070400000,
                                                                                  u'key_as_string': u'2015-01-01'}]},
                                                         u'doc_count': 1,
                                                         u'key': u'clinicaltrials'},
                                                        {u'dates': {u'buckets': [{u'doc_count': 0,
                                                                                  u'key': 1388534400000,
                                                                                  u'key_as_string': u'2014-01-01'},
                                                                                 {u'doc_count': 0,
                                                                                  u'key': 1420070400000,
                                                                                  u'key_as_string': u'2015-01-01'}]},
                                                         u'doc_count': 0,
                                                         u'key': u'arxiv_oai'}],
                                           u'doc_count_error_upper_bound': 0,
                                           u'sum_other_doc_count': 0}}],
                 u'doc_count_error_upper_bound': 5860,
                 u'sum_other_doc_count': 706643}
       }})

    my_search.execute = Mock(return_value=search_mock)
    my_results = my_search.execute()
    my_dataframe = convert_nested_to_dataframe(my_results.aggregations)
    assert my_dataframe.shape == (18, 4)
    for tag_buckets in my_results.aggregations.tags.buckets:
        assert tag_buckets.key in my_dataframe['tags'].values.tolist()
        for source_buckets in tag_buckets.source.buckets:
            assert source_buckets.key in my_dataframe['source'].values.tolist()
            for dates_buckets in source_buckets.dates.buckets:
                assert dates_buckets.dates in my_dataframe['dates'].values.tolist()


def test_convert_nested_to_dataframe_raise_ValueError():

    return

    #FIXME currently this search breaks sharepa, no sure why, but needed to raise the value error

    my_search = ShareSearch()  # BASE_URL='https://staging.osf.io/api/v1/share/search/')

    # first we test crossed data
    my_search.aggs.bucket(
        'tags',  # Every aggregation needs a name
        'terms',
        field='tags',
        size=3,
        min_doc_count=0,
    ).bucket(
        'source',
        'terms',
        field='source',
        size=3,
        min_doc_count=0
    ).bucket(
        'tags2',
        'terms',
        field='tags',
        size=10,
        min_doc_count=0
    ).bucket(
        'dates',
        'date_histogram',
        field='providerUpdatedDateTime',
        interval='1y',
        format='yyyy-MM-dd',
        extended_bounds={
            "min": "2014-01-01",
            "max": "2015-01-01"},
        min_doc_count=0
    )

    #TODO create Mock return object for my_search.execute() here
    my_results = my_search.execute()
    my_dataframe = convert_nested_to_dataframe(my_results.aggregations)
    print(my_dataframe)

