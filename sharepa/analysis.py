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


def merge_dataframes(*dfs):
    '''A helper function for merging two dataframes that have the same indices

        :param dfs: a list of dataframes to be merged (note: they must have the same indices)
        :type dfs: list[pandas.DataFrame]
        :returns: pandas.DataFrame -- a merged dataframe
    '''
    return pd.concat(dfs, axis=1, join_axes=[dfs[0].index])
