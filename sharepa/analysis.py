import pandas as pd


def bucket_to_dataframe(name, buckets, append_name=None):
    '''A function that turns elasticsearch aggregation buckets into dataframes

        :param name: The name of the bucket (will be a column in the dataframe)
        :type name: str
        :param bucket: a bucket from elasticsearch results
        :type bucket: list[dict]
        :returns: pandas.DataFrame
    '''
    expanded_buckets = []
    for item in buckets:
        if type(item) is dict:
            single_dict = item
        else:
            single_dict = item.to_dict()
        single_dict[name] = single_dict.pop('doc_count')
        if append_name:
            for key in single_dict.keys():
                single_dict[append_name + '.' + key] = single_dict.pop(key)
        expanded_buckets.append(single_dict)
    return pd.DataFrame(expanded_buckets)


def agg_to_two_dim_dataframe(agg):
    '''A function that takes an elasticsearch response with aggregation and returns the names of all bucket value pairs

        :param agg: an aggregation from elasticsearch results
        :type agg: elasticsearch response.aggregation.agg_name object
        :returns: pandas data frame of one or two dimetions depending on input data
    '''
    expanded_agg = []
    for bucket in agg.buckets:
        bucket_as_dict = bucket.to_dict()
        if dict not in [type(item) for item in bucket_as_dict.values()]:
            return bucket_to_dataframe('doc_count', agg.buckets)
        else:
            name_of_lower_level = bucket_as_dict.keys()[0]
            single_level_dataframe = bucket_to_dataframe(bucket.key,
                                                         bucket[name_of_lower_level]['buckets'],
                                                         name_of_lower_level)
            expanded_agg.append(single_level_dataframe)
    merged_results = merge_dataframes(*expanded_agg)
    # rearrange to get key as first col
    cols = merged_results.columns.tolist()
    indices_of_keys = [i for i, s in enumerate(cols) if 'key' in s]
    all_other_cols = [i for i in range(0, len(cols)) if i not in indices_of_keys]
    new_col_order = indices_of_keys + all_other_cols
    return merged_results[new_col_order]


def merge_dataframes(*dfs):
    '''A helper function for merging two dataframes that have the same indices, duplicate columns are removed

        :param dfs: a list of dataframes to be merged (note: they must have the same indices)
        :type dfs: list[pandas.DataFrame]
        :returns: pandas.DataFrame -- a merged dataframe
    '''
    merged_dataframe = pd.concat(dfs, axis=1, join_axes=[dfs[0].index])
    return merged_dataframe.transpose().drop_duplicates().transpose()
