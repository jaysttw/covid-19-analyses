import datetime as dt
import numpy as np
import pandas as pd

REPO_PATH = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
CSSE_DATA_PATH = REPO_PATH + "csse_covid_19_data/"
TIME_SERIES_PATH = CSSE_DATA_PATH + "csse_covid_19_time_series/"

CSV_URL = {}
CSV_URL['CONFIRMED'] = "time_series_covid19_confirmed_global.csv"
CSV_URL['DEATHS'] = "time_series_covid19_deaths_global.csv"
CSV_URL['RECOVERED'] = "time_series_covid19_recovered_global.csv"
CSV_URL['US_CONFIRMED'] = "time_series_covid19_confirmed_US.csv"
CSV_URL['US_DEATHS'] = "time_series_covid19_deaths_US.csv"


def _process_columns(col_name):
    '''
    Formats the column entries in the JHU CSSE raw data to datetime format, returning the original value if not a date.
    Parameters
    ----------
    col_name : str
        Name of the original column.

    Returns
    -------
    str or datetime.date
        Either a string with the original column name, if conversion fails, or the converted datetime.date value.

    '''
    try:
        return dt.datetime.strptime(col_name, '%m/%d/%y').date()
    except ValueError:
        try:
            return dt.datetime.strptime(col_name, '%m/%d/%Y').date()
        except ValueError:
            return col_name

def global_case_data(path = None):
    '''
    Returns the JHU CSSE data on country-level.

    Parameters
    ----------
    path : str
        Path to the JHU CSSE data with confirmed cases. Defaults to `TIME_SERIES_PATH + CSV_URL['CONFIRMED']`.

    Returns
    -------
    df_by_country : pandas.DataFrame
        Pandas DataFrame of the case numbers for each country.

    '''
    if path is None: path = TIME_SERIES_PATH + CSV_URL['CONFIRMED']
    df_confirmed = pd.read_csv(path)
    df_by_country = (pd.pivot_table(df_confirmed.drop(columns=['Lat', 'Long', 'Province/State']),
                                    index=['Country/Region'],
                                    aggfunc=np.sum
                                    )
                     .rename(columns=_process_columns)
                     .transpose()
                     .sort_index()
                     )
    return df_by_country


def first_crossed(df, threshold):
    '''Takes a "tidy" dataframe and a threshold, and returns the date after which the values exceed the threshold.


    '''

    def inner_first_crossed(series, threshold):
        try:
            result = series[series > threshold].index[0]
            return result
        except IndexError:
            return np.nan

    result = df.apply(func=inner_first_crossed, args=[threshold]).dropna()
    return result


def align_cases(df, threshold):
    '''

    '''
    temp = first_crossed(df, threshold)
    result = pd.DataFrame(data=[df[x][temp[x] - dt.timedelta(1):].values for x in temp.index]).transpose()
    result.columns = [x for x in temp.index]
    return result


def train_val_test_split(df):
    '''Splits the input dataframe into train, validation, and test. This function first defines an inner function that
    operates on a column, returning three dataframes containing the respective sets.

    '''

    dates_of_first_cases = first_crossed(df, 1)
    days_with_cases = {x: len(df[x][dates_of_first_cases[x] - dt.timedelta(1):]) for x in dates_of_first_cases.index}

    shortest_run = days_with_cases[min(days_with_cases, key=days_with_cases.get)]

    test_len = int(shortest_run/5)
    train_len = len(df) - (2 * test_len)

    # def _process_column(df, seq_length: int, col: str):
    #     print(f"Processing: {col}")
    #     temp = df[col].dropna()
    #     n = len(temp) - seq_length + 1
    #     result = [temp[x:x + seq_length] for x in range(n)]
    #     test_len = int(n / 5)
    #     train_len = n - (2 * test_len)
    #     return (result[:train_len], result[train_len:train_len + test_len], result[train_len + test_len:])
    #
    # # train_set = []
    # # val_set = []
    # # test_set = []
    # #
    # # for col in df.columns:
    # #     train_temp, val_temp, test_temp = _process_column(df, seq_length, col)
    # #     train_set += train_temp
    # #     val_set += val_temp
    # #     test_set += test_temp
    # #
    # # train_set = pd.DataFrame([x.reset_index(drop=True) for x in train_set])
    # # val_set = pd.DataFrame([x.reset_index(drop=True) for x in val_set])
    # # test_set = pd.DataFrame([x.reset_index(drop=True) for x in test_set])

    train_set = df.iloc[:, :train_len]
    val_set = df.iloc[:, train_len:train_len+test_len]
    test_set = df.iloc[:, train_len+test_len:]
    return train_set, val_set, test_set

def train_val_test_sequences(df, seq_length: int):
    results = []
    for col in df.columns: 
        results.append([df[col][x:seq_length] for x in range(len(df) - seq_length + 1)])
    return result

# # Unused code
# df_us_confirmed = (pd.read_csv(TIME_SERIES_PATH + CSV_URL['US_CONFIRMED'])
#                    .rename(columns={'Long_': 'Long',
#                                     'Country_Region': 'Country/Region',
#                                     'Province_State': 'Province/State'
#                                    })
#                   )