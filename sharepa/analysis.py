import pandas as pd


def bucket_to_dataframe(name, bucket):
    '''A function that turns elasticsearch aggregation buckets into dataframes

        :param name: The name of the bucket (will be a column in the dataframe)
        :type name: str
        :param bucket: a bucket from elasticsearch results
        :type bucket: list[dict]
        :returns: pandas.DataFrame
    '''
    return pd.DataFrame(
        {item['key']: item['doc_count'] for item in bucket},
        index=[name]
    ).T


def convert_key(x):
    x.key = x.key_as_string
    return x


def aggregation_to_dataframe(name,agg,filter=None):
    '''A function that turns elasticsearch response with/without aggregation into a dataframe

        :param name: The name of the returned dataframe col
        :type name: str
        :param bucket: a bucket from elasticsearch results
        :type bucket: list[dict]
        :returns: pandas.DataFrame
    '''
    if hasattr(agg, 'buckets'):
        if filter is not None:
            expanded_agg = []
            for bucket in agg.buckets:
                expanded_agg.append(bucket_to_dataframe(bucket.key, map(convert_key, getattr(bucket,filter).buckets)))
            return merge_dataframes(*expanded_agg)
        else:
            return bucket_to_dataframe(name,agg.buckets)
    else:
        raise NameError('no aggregated data to convert') #FIXME Work out what i should actually throw here



def merge_dataframes(*dfs):
    '''A helper function for merging two dataframes that have the same indices

        :param dfs: a list of dataframes to be merged (note: they must have the same indices)
        :type dfs: list[pandas.DataFrame]
        :returns: pandas.DataFrame -- a merged dataframe
    '''
    return pd.concat(dfs, axis=1, join_axes=[dfs[0].index])
