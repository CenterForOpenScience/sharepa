# sharepa

```master``` build status: [![Build Status](https://travis-ci.org/fabianvf/sharepa.svg?branch=master)](https://travis-ci.org/fabianvf/sharepa)


```develop``` build status: [![Build Status](https://travis-ci.org/fabianvf/sharepa.svg?branch=develop)](https://travis-ci.org/fabianvf/sharepa)


[![Coverage Status](https://coveralls.io/repos/fabianvf/sharepa/badge.svg?branch=develop)](https://coveralls.io/r/fabianvf/sharepa?branch=develop)
[![Code Climate](https://codeclimate.com/github/fabianvf/sharepa/badges/gpa.svg)](https://codeclimate.com/github/sharepa/scrapi)


A python client for browsing and analyzing SHARE data (https://osf.io/share), gathered with scrAPI (https://github.com/fabianvf/scrapi). It builds heavily (almost completely) on the [elasticsearch-dsl](https://github.com/elastic/elasticsearch-dsl-py) package for handling Elasticsearch querying and aggregations, and contains some additional utilities to help with graphing and analyzing the data.

## Installation
You can install sharepa using pip:
```pip install sharepa```

## Aggregations Vs Results


## Getting Started
Here are some basic searches to get started parsing through SHARE data.

### Basic Search
A basic search will provide access to all documents in SHARE - in 10 document slices

#### Count
You can use sharepa to get the total number of documents in SHARE
```
from sharepa import basic_search


print(basic_search.count()
```

#### Iterating through results
Executing the basic search will send the actual basic query to the SHARE API and then let you iterate through results

```
results = basic_search.execute()

for hit in results:
    print(hit.title)
```

If we don't want 10 results, or we want to offset the results, we can use slices
```
results = basic_search[5:10].execute()
for hit in results:
    print(hit.title)
```

## Basic Plotting
Sharepa has some basic functions to get you started making plots using [matplotlib](http://matplotlib.org/) and [pandas](http://pandas.pydata.org/).

Raw sharepa data is in the same format as elasticsearch results, represented as a nested structure. To convert the data into a format that pandas can recognize, we have to convert it into a dataframe.

### Creating a dataframe from sharepa data
We can use the bucket_to_dataframe function to convert the elasticsearch formatted data into a pandas dataframe. To do this, we pass the title of the new column, and the place to find the nested data - in this case within ```results.aggregations.sourceAgg.buckets```

```
from sharepa import bucket_to_dataframe


my_data_frame = bucket_to_dataframe('# documents by source', results.aggregations.sourceAgg.buckets)
my_data_frame.plot(kind='bar')
```

This will create a bar graph showing all of the sources, and document counts for each source.

You can also sort the data based on a certain column, in this case, '# documents by source'

```
my_data_frame.sort(ascending=False, columns='# documents by source').plot(kind='bar')
```

## Advanced Search
You can make your own search object, which allows you to pass in custom queries for certain terms or SHARE fields. Queries are formed using [lucene query syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). 

```
my_search = ShareSearch()

my_search = my_search.query(
    'query_string', # Type of query, will accept a lucene query string
    query='NOT tags:*', # This lucene query string will find all documents that don't have tags
    analyze_wildcard=True  # This will make elasticsearch pay attention to the asterisk (which matches anything)
)

new_results = my_search.execute()
for hit in new_results:
    print(hit.title)
```

This type of query accepts a 'query_string'. Other options include a [match query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html), a [multi-match query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html), a [bool query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html), and any other query structure available in the elasticsearch API.

## Aggregations for data analysis
While searching for individual results is useful, sharepa also lets you make aggregation queries that give you results across the entirety of the SHARE dataset at once. This is useful if you're curious about the completeness of data sets. For example, we can find the number of documents per source that are missing titles. 

We can add an aggregation to my_search that will give us the number 

```
my_search.aggs.bucket(
    'sources',  # Every aggregation needs a name
    'terms',  # There are many kinds of aggregations, terms is a pretty useful one though
    field='_type',  # We store the source of a document in its type, so this will aggregate by source
    size=0,  # These are just to make sure we get numbers for all the sources, to make it easier to combine graphs
    min_doc_count=0
)
```

We can see what query is actually going to be sent to elasticsearch

```
from sharepa.helpers import pretty_print

pretty_print(my_search.to_dict())
```

## Lucene query syntax and Elasticsearch DSL


