import pandas as pd

eq = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) == value)
    
lt = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) < value)
    
gt = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) > value)
    
leq = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) <= value)
    
geq = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) >= value)
    
isin = lambda column, values, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)).isin(values))

def apply_predicates(df, predicates):
    for p in predicates:
        if p is not None: df = df[p(df)]
    return df

def apply_funs(df, funs):
    for f in funs:
        if f is not None: df = f(df)
    return df

def load_df_from_zipped_csv(path, predicates=[], pre_funs=[], post_funs=[], **kwargs):
    if 'iterator' not in kwargs: kwargs['iterator'] = True
    if 'chunksize' not in kwargs: kwargs['chunksize'] = 10000
    if 'compression' not in kwargs: kwargs['compression'] = 'zip'
    if 'header' not in kwargs: kwargs['header'] = 0
    if 'dtype' not in kwargs: kwargs['dtype'] = str
    if 'keep_default_na' not in kwargs: kwargs['keep_default_na'] = False
    it = pd.read_csv(path, **kwargs)
    df = pd.concat([apply_funs(apply_predicates(apply_funs(chunk, pre_funs), predicates), post_funs) for chunk in it])
    # Since we are reading the data chunk by chunk and then concatenating the resulting data frames, the indices may not
    # be unique. We correct this by replacing them:
    df.index = range(len(df))
    return df

def detect_df_column_types(df):
    for c in df.columns:
        print(c)
    return None

def convert_df_columns(df, conversions, in_place=False):
    if not in_place: df = df.copy()
    conversion_columns = set(conversions.keys())
    unfamiliar_columns = conversion_columns.difference(df.columns)
    assert len(unfamiliar_columns) == 0, 'Unfamiliar columns: %s' % str(unfamiliar_columns)
    for column, conversion in conversions:
        df[column] = conversion(df[column])
    return df
    for col, conversion in conversions:
        df[col] = df[col].apply(conversion)
    return df
