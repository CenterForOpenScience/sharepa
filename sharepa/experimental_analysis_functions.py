import pandas as pd


def convert_nested_to_dataframe(agg, dates_as_key=True):
    '''A function that takes nested elasticsearch response with aggregation and returns a nested dataframe
        Warning: This is a recursive function, and rather non-intuitive to understand

        This function takes nested and crossed aggregations and converts them to an easy to manipulates pandas dataframe
         e.g. Here we have a gender aggregation nested in year which is nested in state

        the output we want:

        state        year       gender      doc_count
        CA           2000       male        2
        CA           2000       female      5
        CA           2001       male        5
        CA           2001       female      5
        CA           2002       male        5
        CA           2002       female      5
        MN           2000       male        2
        MN           2000       female      5
        MN           2001       male        5
        MN           2001       female      5
        MN           2002       male        5
        MN           2002       female      5
        NY           2000       male        2
        NY           2000       female      5
        NY           2001       male        5
        NY           2001       female      5
        NY           2002       male        5
        NY           2002       female      5

        What we do is step down through all the layers of nested data (recursively) until we reach the end,
        and from the end, start creating pandas dataframes that get merged back into one giant dataframe

        this function is in an experimental state, and currently only tested on 3 nested levels,
        TODO crossed data does not work
        :param agg: an aggregation from elasticsearch results with nesting
        :type agg: elasticsearch response.aggregation object
        :returns: pandas data frame like example above, with nested data
    '''
    crossed_cats_expanded = []
    high_level_returning = False
    agg_as_dict = agg.to_dict()
    cat_names = [item for item in agg_as_dict.keys() if type(agg_as_dict[item]) is dict]
    for cat_name in cat_names:  # TODO deal with multiple aggregations at the same level (Crossing)
        expanded_buckets = []
        merge_vert = False
        if not len(getattr(agg, cat_name).buckets):
            raise ValueError('There is no count data in the lowest level of nesting. Is your search setup correctly?')

        for bucket in getattr(agg, cat_name).buckets:
            bucket_as_dict = bucket.to_dict()
            if dict not in [type(item) for item in bucket_as_dict.values()]:
                # we are at lowest level, begin return
                if ('key_as_string' in bucket_as_dict.keys()) and dates_as_key:  # change dates to readble format
                    bucket_as_dict['key'] = bucket['key_as_string']
                    bucket_as_dict.pop('key_as_string')

                bucket_as_dict[cat_name] = bucket_as_dict.pop(
                    'key')  # change the name of the key to something meaningful
                expanded_buckets.append(bucket_as_dict)  # combine each dict at the lowest level
            else:
                # We are at some level other than the lowest
                level_name = str(bucket.key)  # save the name of this level
                lower_level_return = convert_nested_to_dataframe(bucket)  # and drop down into the next level
                expanded_buckets.append(add_category_labels(level_name,cat_name,lower_level_return))
                merge_vert = True
        if not merge_vert:
            dataframe_out = pd.DataFrame(expanded_buckets)
            dataframe_out.rename(columns=lambda x: x.replace('key', cat_name))
            crossed_cats_expanded.append(dataframe_out.reset_index(drop=True))
            high_level_returning = True

    if high_level_returning:
        return pd.concat(crossed_cats_expanded, axis=1).reset_index(drop=True)
    else:
        return pd.concat(expanded_buckets, axis=0).reset_index(drop=True)


def add_category_labels(level_name,cat_name,dataframe_needing_cat):
    '''A function that adds a category name column to a pandas dataframe

        :param level_name: an aggregation from elasticsearch results with nesting
        :type level_name: elasticsearch response.aggregation object
        :param cat_name: an aggregation from elasticsearch results with nesting
        :type cat_name: elasticsearch response.aggregation object
        :param dataframe_needing_cat: a pandas dataframe to append category name too
        :type dataframe_needing_cat: elasticsearch response.aggregation object
        :returns: pandas data frame like example above, with nested data
    '''
    cat_name_dataframe = pd.DataFrame(
        [level_name for i in range(0, dataframe_needing_cat.shape[0])])  # create a cat name column
    cat_name_dataframe.columns = [cat_name]  # name the column something meaningful
    return pd.concat([cat_name_dataframe, dataframe_needing_cat], axis=1)
