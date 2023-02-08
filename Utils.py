import pandas as pd


def remove_missing(df: object) -> object:
    '''
    Removes rows with missing values 
    
    Args:
        df: a pandas dataframe
 
    Raises:
        TypeError: if anything other than a dataframe is passed
 
    Returns:
        A pandas dataframe
    '''

    if not isinstance(df, pd.DataFrame):
        raise TypeError('Input must be a Pandas DataFrame')

    return df.dropna().copy()


def date_formatting(df: object) -> object:
    '''
    Transforms columns with dates from any format into standard format and datetime type  
    
    Args:
        df: a pandas dataframe or series
 
    Raises:
        TypeError: if anything other than a dataframe or series is passed
 
    Returns:
        A pandas dataframe
    '''
    if not isinstance(df, pd.DataFrame) and not isinstance(df, pd.Series):
        raise TypeError('Input must be a Pandas DataFrame or Series')

    return df.apply(pd.to_datetime)


def extract_year(df: object) -> object:
    '''
    Returns a column with the years of the dates passed as arguments
    
    Args:
        df: a pandas series with datetime values
 
    Raises:
        TypeError: if anything other than a series is passed
        ValueError: if the dtype of the series is not datetime

    Returns:
        A pandas series
    '''
    if not isinstance(df, pd.Series):
        raise TypeError('Input must be a Pandas Series (column)')

    if not df.dtype == 'datetime64[ns]':
        raise ValueError(
            'Input must be a Pandas Series (column) with datetime data')

    return df.dt.year


def categorical_encoding(df: object, dict_map: dict) -> object:
    '''
    Transforms a pandas columns with categorical values with numerical labels
    
    Args:
        df: a pandas series
        dict_map: a dictionary with each category and its numerical equivalent
 
    Raises:
        TypeError: if df is anything other than a series
        TypeError: if dict_map is anything other than a series

    Returns:
        A pandas series
    '''
    if not isinstance(df, pd.Series):
        raise TypeError('First input must be a Pandas Series (column)')

    if not isinstance(dict_map, dict):
        raise TypeError('Second input must be a dictionary')

    return df.map(dict_map)