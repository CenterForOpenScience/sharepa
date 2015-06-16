__author__ = 'admin'
import json
from matplotlib import pyplot
from elasticsearch_dsl import F, A, Q #why these criptic import names

from sharepa.search import ShareSearch
from sharepa.analysis import bucket_to_dataframe, merge_dataframes, aggregation_to_dataframe
# def pretty_print(d):
#     print(json.dumps(d, indent=4))

my_search = ShareSearch()
my_search_two_level_bins = ShareSearch()
# my_search = my_search.query( #this will get everything
#     'query_string',
#     query='tags:*',
#     analyze_wildcard=True
# )

my_search.aggs.bucket(
    'unique_tags',  # Every aggregation needs a name
    'terms',
    field='subjects',  # We store the source of a document in its type, so this will aggregate by source #BYNOTE so this looks at the type feild and agregates by that?
    size=10,  # These are just to make sure we get numbers for all the sources, to make it easier to combine graphs
    min_doc_count=0
)

my_search_two_level_bins.aggs.bucket(
    'unique_tags_with_dates',  # Every aggregation needs a name
    'terms',
    field='subjects',  # We store the source of a document in its type, so this will aggregate by source #BYNOTE so this looks at the type feild and agregates by that?
    size=10,  # These are just to make sure we get numbers for all the sources, to make it easier to combine graphs
    min_doc_count=0
).metric('dates', A('date_histogram', field='providerUpdatedDateTime', interval='1M', format='yyyy-MM-dd'))

#pretty_print(my_search.to_dict())
my_results = my_search.execute()
my_results_two_level_bins = my_search_two_level_bins.execute()

# pretty_print(my_results.aggregations.to_dict())
# for hit in my_results:
#     print hit.title, hit.get('tags')
#
print aggregation_to_dataframe('unique_tags', my_results.aggregations.unique_tags)
print aggregation_to_dataframe('unique_tags_by_date', my_results_two_level_bins.aggregations.unique_tags_with_dates,'dates')
#print aggregation_to_dataframe('unique_tags', my_results.aggregations.unique_tags)
#print bucket_to_dataframe('unique_tags', my_results.aggregations.unique_tags.buckets)
# # unique_tags.plot()
# # pyplot.show()
# #sorted_tags = unique_tags.sort(columns=['',''], )
# #top_tags = sorted_tags[1:40];
# print unique_tags
#
# def eh(x):
#     x.key = x.key_as_string
#     return x
#
# dfs = []
# for bucket in my_results.aggregations.unique_tags.buckets:
#     dfs.append(bucket_to_dataframe(bucket.key, map(eh, bucket.dates.buckets)))



