import json
from elasticsearch_dsl import A

from sharepa import bucket_to_dataframe, ShareSearch


source_agg = A('terms', field='_type', size=0, min_doc_count=0)


def source_counts():
    query = ShareSearch()
    query.aggs.bucket('sourceAgg', source_agg)
    return bucket_to_dataframe(
        'total_source_counts',
        query.execute().aggregations.sourceAgg.buckets
    )


def pretty_print(d):
    print(json.dumps(d, indent=4))
