from elasticsearch_dsl import A

source_agg = A('terms', field='_type', size=0, min_doc_count=0)
