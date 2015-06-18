# sharepa

```master``` build status: [![Build Status](https://travis-ci.org/fabianvf/sharepa.svg?branch=master)](https://travis-ci.org/fabianvf/sharepa)


```develop``` build status: [![Build Status](https://travis-ci.org/fabianvf/sharepa.svg?branch=develop)](https://travis-ci.org/fabianvf/sharepa)


[![Coverage Status](https://coveralls.io/repos/fabianvf/sharepa/badge.svg?branch=develop)](https://coveralls.io/r/fabianvf/sharepa?branch=develop)
[![Code Climate](https://codeclimate.com/github/fabianvf/sharepa/badges/gpa.svg)](https://codeclimate.com/github/fabianvf/sharepa)


A python client for browsing and analyzing SHARE data (https://osf.io/share), gathered with scrAPI (https://github.com/fabianvf/scrapi). It builds heavily (almost completely) on the [elasticsearch-dsl](https://github.com/elastic/elasticsearch-dsl-py) package for handling Elasticsearch querying and aggregations, and contains some additional utilities to help with graphing and analyzing the data.

## Installation
You can install sharepa using pip:
```pip install sharepa```

## Getting Started
Here are some basic searches to get started parsing through SHARE data.

### Basic Search
A basic search will provide access to all documents in SHARE - in 10 document slices.

#### Count
You can use sharepa and the basic search to get the total number of documents in SHARE
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

## Advanced Search
You can make your own search object, which allows you to pass in custom queries for certain terms or SHARE fields. Queries are formed using [lucene query syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). 

```
my_search = ShareSearch()

my_search = my_search.query(
    'query_string', # Type of query, will accept a lucene query string
    query='NOT tags:*', # This lucene query string will find all documents that don't have tags
    analyze_wildcard=True  # This will make elasticsearch pay attention to the asterisk (which matches anything)
)
```

This type of query accepts a 'query_string'. Other options include a [match query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html), a [multi-match query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html), a [bool query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html), and any other query structure available in the elasticsearch API.

We can see what that query that we're about to send to elasticsearch by using the pretty print helper function:

```
from sharepa.helpers import pretty_print


pretty_print(my_search.to_dict())
```

```
{
    "query": {
        "query_string": {
            "analyze_wildcard": true, 
            "query": "NOT tags:*"
        }
    }
}
```


When you execute that query, you can then iterate through the results the same way that you could with the simple search query.
```
new_results = my_search.execute()
for hit in new_results:
    print(hit.title)
```


## Aggregations for data analysis
While searching for individual results is useful, sharepa also lets you make aggregation queries that give you results across the entirety of the SHARE dataset at once. This is useful if you're curious about the completeness of data sets. For example, we can find the number of documents per source that are missing titles. 

We can add an aggregation to my_search that will give us the number of documents per source that meet that previously defined search query (in our case, items that don't have tags). Here's what adding that aggregation will look like - 

```
my_search.aggs.bucket(
    'sources',  # Every aggregation needs a name
    'terms',  # There are many kinds of aggregations, terms is a pretty useful one though
    field='_type',  # We store the source of a document in its type, so this will aggregate by source
    size=0,  # These are just to make sure we get numbers for all the sources, to make it easier to combine graphs
    min_doc_count=0
)
```

We can see which query is actually going to be sent to elasticsearch by printing out the query.

```
pretty_print(my_search.to_dict())
```

```
{
    "query": {
        "query_string": {
            "analyze_wildcard": true, 
            "query": "NOT tags:*"
        }
    }, 
    "aggs": {
        "sources": {
            "terms": {
                "field": "_type", 
                "min_doc_count": 0, 
                "size": 0
            }
        }
    }
}
```

This is the actual query that will be sent to the SHARE API. You can see that it added a section called "aggs" to the basic query that we made earlier.

You can access the aggregation data for basic plotting, and analysis, by accessing the bucket 

## Basic Plotting
Sharepa has some basic functions to get you started making plots using [matplotlib](http://matplotlib.org/) and [pandas](http://pandas.pydata.org/).

Raw sharepa data is in the same format as elasticsearch results, represented as a nested structure. To convert the data into a format that pandas can recognize, we have to convert it into a dataframe.

### Creating a dataframe from sharepa data
We can use the bucket_to_dataframe function to convert the elasticsearch formatted data into a pandas dataframe. To do this, we pass the title of the new column we want created, and the place to find the nested aggregation data.

Let's re-execute the my_search command including the updated query and update the new_results variable.

```
new_results = my_search.execute()
```

To convert these results to a pandas dataframe, we'll look within the appropriate results search bucket, in this case within ```new_results.aggregations.sourceAgg.buckets```

```
from sharepa import bucket_to_dataframe


my_data_frame = bucket_to_dataframe('# documents by source - No Tags', new_results.aggregations.sources.buckets)
my_data_frame.plot(kind='bar')
```

This will create a bar graph showing all of the sources, and document counts for each source matching our query of items that do not have tags.

You can also sort the data based on a certain column, in this case, '# documents by source - No Tags'

```
my_data_frame.sort(ascending=False, columns='# documents by source - No Tags').plot(kind='bar')
```


## Advanced Aggregations

Let's make a more interesting aggregation. Let's look at the documents that are missing titles, by source.

```
my_search.aggs.bucket(
    'missingTitle',  # Name of the aggregation
    'filters', # We'll want to filter all the documents that have titles
    filters={ 
        'missingTitle': F(  # F defines a filter
            'fquery',  # This is a query filter which takes a query and filters document by it
            query=Q(  # Q can define a query
                'query_string', # The type of aggregation
                query='NOT title:*',  # This will match all documents that don't have content in the title field
                analyze_wildcard=True,
            )
        ) 
    }
).metric(  # but wait, that's not enough! We need to break it down by source as well
    'sourceAgg',
    'terms',
    field='_type',
    size=0,
    min_doc_count=0
)
```

We can check out what the query looks like now: 
```
pretty_print(my_search.to_dict()) 
```

```
{
    "query": {
        "query_string": {
            "analyze_wildcard": true, 
            "query": "NOT tags:*"
        }
    }, 
    "aggs": {
        "sources": {
            "terms": {
                "field": "_type", 
                "min_doc_count": 0, 
                "size": 0
            }
        }, 
        "missingTitle": {
            "aggs": {
                "sourceAgg": {
                    "terms": {
                        "field": "_type", 
                        "min_doc_count": 0, 
                        "size": 0
                    }
                }
            }, 
            "filters": {
                "filters": {
                    "missingTitle": {
                        "fquery": {
                            "query": {
                                "query_string": {
                                    "query": "NOT title:*", 
                                    "analyze_wildcard": true
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
```

Wow this query has gotten big! Good thing we don't have to define it by hand.

Now we just need to execute the search:
```
my_results = my_search.execute()
```

Let's check out the results, and make sure that there are indeed no tags.

```
for hit in my_results:
    print(hit.title, hit.get('tags'))  # we can see there are no tags in our results
```

Let's pull out those buckets and turn them into dataframes for more analysis

```
missing_title = bucket_to_dataframe('missingTitle', my_results.aggregations.missingTitle.buckets.missingTitle.sourceAgg.buckets)
matches = bucket_to_dataframe('matches', my_results.aggregations.sources.buckets)
```

It'd be great if we could merge this dataframe with another that has information about all of the documents. Luckilly we have a built in function that will give us that data frame easily, called source_counts. 

We can use that dataframe and merge it with our newly created one:

```
from sharepa import source_counts


merged = merge_dataframes(source_counts(), matches,  missing_title)
```

We can also easily do computations on these columns, and add those to the dataframe. Here's a way to get a pandas dataframe with a column for a percent from each source that is missing tags and a title:

```
merged['percent_missing_tags_and_title'] = (merged.missingTitle / merged.total_source_counts) * 100
```
