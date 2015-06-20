import json
from sharepa.search import ShareSearch
from sharepa.experimental_analysis_functions import convert_nested_to_dataframe

def pretty_print(d):
    print(json.dumps(d, indent=4))

my_search = ShareSearch()
my_search_two_level_bins = ShareSearch()
my_search_two_level_bins.aggs.bucket(
    'tags',  # Every aggregation needs a name
    'terms',
    field='tags',
    # We store the source of a document in its type, so this will aggregate by source #BYNOTE so this looks at the type feild and agregates by that?
    size=10,  # These are just to make sure we get numbers for all the sources, to make it easier to combine graphs
    min_doc_count=0,
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
        "max": "2015-06-01"},
    min_doc_count=0
)

my_results_two_level_bins = my_search_two_level_bins.execute()
print(convert_nested_to_dataframe(my_results_two_level_bins.aggregations))
