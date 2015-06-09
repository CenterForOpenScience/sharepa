import json
import requests

from elasticsearch_dsl import Search
from elasticsearch_dsl.result import Response


class ShareSearch(Search):
    BASE_URL = 'https://osf.io/api/v1/share/search/'
    HEADERS = {'content-type': 'application/json'}
    PARAMS = dict(raw=True)

    def execute(self):
        return Response(
            self._query(self.to_dict()),
            callbacks=self._doc_type_map
        )

    def count(self):
        d = self.to_dict()
        if d.get('aggs'):
            del d['aggs']
        self = ShareSearch.from_dict(d)
        return self._query(self.to_dict(), params=dict(count=True))['count']

    def scan(self, size=100):
        count = 0
        page = list(self[0:size].execute())
        while(page):
            for hit in page:
                count += 1
                yield hit
            page = list(self[count:count + size].execute())

    def _query(self, data, params=None):
        return requests.post(
            self.BASE_URL,
            headers=self.HEADERS,
            data=json.dumps(self.to_dict()),
            params=params or self.PARAMS
        ).json()

basic_search = ShareSearch()
basic_search.aggs.bucket(
    'sourceAgg',
    'terms',
    field='_type',
    size=0,
    min_doc_count=0
)
