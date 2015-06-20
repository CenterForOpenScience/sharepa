
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

        What we want to do is step down through all the layers of nested data (recursively) until we reach the end,
        and from the end, start creating pandas dataframes that get merged back into one giant dataframe

        this function is in an experimental state, and currently only tested on 2 nested levels, crossed date does not work
        :param agg: an aggregation from elasticsearch results
        :type agg: elasticsearch response.aggregation.agg_name object
        :returns: pandas data frame of one or two dimetions depending on input data
    '''
    agg_as_dict = agg.to_dict()
    cat_names = [item for item in agg_as_dict.keys() if type(agg_as_dict[item]) is dict]
    for cat_name in cat_names: #FIXME deal with multiple aggergations at the same level
        expanded_buckets = []
        merge_vert = False
        for bucket in getattr(agg, cat_name).buckets:
            bucket_as_dict = bucket.to_dict()
            if dict not in [type(item) for item in bucket_as_dict.values()]:
                # we are at lowest level, begin return
                if ('key_as_string' in bucket_as_dict.keys()) and dates_as_key: #change dates to readble format
                    bucket_as_dict['key'] = bucket['key_as_string']

                bucket_as_dict[cat_name] = bucket_as_dict.pop('key') #change the name of the key to something meaningful
                expanded_buckets.append(bucket_as_dict) #combine each dict at the lowest level

            else:
                #We are at some level other than th lowest
                level_name = str(bucket.key) #save the name of this level
                lower_level_return = convert_nested_to_dataframe(bucket) #and drop down into the next level
                cat_name_dataframe = pd.DataFrame([level_name for i in range(0,lower_level_return.shape[0])]) #create a cat name column
                cat_name_dataframe.columns = [cat_name] #name the column something meaningful
                merged_names_dataframe = pd.concat([cat_name_dataframe, lower_level_return], axis=1) #add return dataframes from lower levels, and attach the cat name coloum
                expanded_buckets.append(merged_names_dataframe) #combine each cat and its data
                merge_vert = True
        # if merge_vert:
        #     dataframe_out = pd.concat(expanded_buckets, axis=0)
        #     return dataframe_out
        if not merge_vert:
            dataframe_out = pd.DataFrame(expanded_buckets)
            dataframe_out.rename(columns=lambda x: x.replace('key', cat_name))
            return dataframe_out # FIXME this return here means we cannot add in other catogories at the same level (cant deal with corssing)
    return pd.concat(expanded_buckets, axis=0)
