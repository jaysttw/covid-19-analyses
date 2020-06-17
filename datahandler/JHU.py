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

# # Unused code
# df_us_confirmed = (pd.read_csv(TIME_SERIES_PATH + CSV_URL['US_CONFIRMED'])
#                    .rename(columns={'Long_': 'Long',
#                                     'Country_Region': 'Country/Region',
#                                     'Province_State': 'Province/State'
#                                    })
#                   )