from sharepa.analysis import merge_dataframes

import pandas as pd


def test_merge_dataframes():
    dream = pd.DataFrame({'Rhodes': 'Dusty'}, index=['Rhodes'])
    stardust = pd.DataFrame({'Rhodes': 'Cody'}, index=['Rhodes'])

    family = merge_dataframes(dream, stardust)

    assert isinstance(family, pd.core.frame.DataFrame)
    assert family.columns.values.tolist() == ['Rhodes', 'Rhodes']
