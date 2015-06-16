from sharepa.helpers import source_agg
from sharepa.search import ShareSearch, basic_search  # noqa
from sharepa.analysis import bucket_to_dataframe, merge_dataframes  # noqa


def source_counts():
    query = ShareSearch()
    query.aggs.bucket('sourceAgg', source_agg)
    return bucket_to_dataframe(
        'total_source_counts',
        query.execute().aggregations.sourceAgg.buckets
    )
