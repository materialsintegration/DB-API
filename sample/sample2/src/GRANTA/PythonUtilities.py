# -*- coding: utf-8 -*-

# ****************************************************
# * PythonUtilities.py
# *
# *    python submodule script
# *
# *  2019/12/13  T.Noguchi  create
# *  
# *  
# *
# ****************************************************

import sys
import os
import pandas as pd

# -----------------------------------
# module variable
# -----------------------------------



# -----------------------------------
# local function
# -----------------------------------



# -----------------------------------
# modules
# -----------------------------------
# dataframe multi header columns
def multi_headers(in_df):
    '''
    reshape multi header dataframe

    [args]
      in_df            : dataframe

    [return]
      dataframe
    '''

    # init    
    df = in_df.copy()
    if type(df.columns) is not pd.MultiIndex:
        return df

    # remove Unnamed and reindex
    df = df.rename(columns=lambda x: x if not 'Unnamed' in str(x) else '')
    df = df.reset_index()

    cols = df.columns
    copy_col = list(cols)

    # move column.names to matrix top
    #copy_col[0] = tuple([(name if name is not None else '') \
    #                     for name in cols.names])
    
    # come near top with empty cell
    for i, col in enumerate(copy_col):
        pack = [content for content in col if content != '']
        copy_col[i] = tuple(pack + ([''] * (len(col) - len(pack))))

    df.columns = pd.MultiIndex.from_tuples(copy_col)
    cols.names = tuple([None for x in cols.names])

    return df







