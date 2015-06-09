from sharepa.search import ShareSearch, basic_search  # noqa
from sharepa.analysis import bucket_to_dataframe, merge_dataframes  # noqa


def source_counts():
    return bucket_to_dataframe(
        'total_source_counts',
        basic_search.execute().aggregations.sourceAgg.buckets
    )
