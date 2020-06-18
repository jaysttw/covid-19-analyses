import datetime as dt
#import numpy as np
import pandas as pd
import zipfile as zf
import csv
import io
import itertools
import os
import requests

# World Bank population data paths
WORLDBANK_API_URL = "http://api.worldbank.org/v2/en/indicator/"
WORLDBANK_API_CSV = "?downloadformat=csv"

def _worldbank_url(wb_code):
    return WORLDBANK_API_URL + wb_code + WORLDBANK_API_CSV

# # These constants should ideally not be used in the functions.
# WORLDBANK_POP_CODE = "SP.POP.TOTL"
# WORLDBANK_POP_ZIP = _worldbank_url(WORLDBANK_POP_CODE)
# WORLDBANK_URBPOP_CODE = "SP.URB.TOTL.IN.ZS"
# WORLDBANK_URB_POP_ZIP = _worldbank_url(WORLDBANK_URBPOP_CODE)

# Dict to rename countries obtained here to match the JHU CSSE dataset.
WORLDBANK_COUNTRIES = {
    'Saint Kitts and Nevis': 'St. Kitts and Nevis',
    'Diamond Princess': '',
    'Congo (Kinshasa)': 'Congo, Dem. Rep.',
    'Korea, South': 'Korea, Rep.',
    'MS Zaandam': '',
    'Russia': 'Russian Federation',
    'Egypt': 'Egypt, Arab Rep.',
    'Venezuela': 'Venezuela, RB',
    'US': 'United States',
    'Syria': 'Syrian Arab Republic',
    'Kyrgyzstan': 'Kyrgyz Republic',
    'Yemen': 'Yemen, Rep.',
    'Gambia': 'Gambia, The',
    'Holy See': '',
    'Slovakia': 'Slovak Republic',
    'Laos': 'Lao PDR',
    'Congo (Brazzaville)': 'Congo, Rep.',
    'Czechia': 'Czech Republic',
    'Iran': 'Iran, Islamic Rep.',
    'Western Sahara': '',
    'Saint Lucia': 'St. Lucia',
    'Bahamas': 'Bahamas, The',
    'Taiwan*': '', # https://datahelpdesk.worldbank.org/knowledgebase/topics/19280-country-classification
    'Burma': 'Myanmar',
    'Saint Vincent and the Grenadines': 'St. Vincent and the Grenadines',
    'Brunei': 'Brunei Darussalam'
}

def _retrieve_worldbank(wb_code):
    worldbank_pop_request = requests.get(_worldbank_url(wb_code))
    with zf.ZipFile(io.BytesIO(worldbank_pop_request.content), 'r') as wb_pop_zip:
        wb_pop_zip.extractall('tmp')
    raw_csvs = [x for x in os.listdir('tmp') if x.startswith("API_" + wb_code)]
    file_dates = {}
    for file in raw_csvs:
        with open('tmp/' + file) as csvfile:
            reader = csv.reader(csvfile)
            for row in itertools.islice(reader, 2, 3):
                file_dates[file] = dt.datetime.strptime(row[1], "%Y-%m-%d").date()
    return pd.read_csv("tmp/" + max(file_dates), skiprows=3, index_col="Country Name").iloc[:, :-2]

def latest_worldbank(wb_code):
    return _retrieve_worldbank(wb_code).iloc[:, [0, -1]].rename(index={v:k for (k,v) in WORLDBANK_COUNTRIES.items()})


def calculate_case_rate(cases, population):
    result = cases.copy()
    for col in cases.columns:
        try:
            result[col] = 1000000 * cases[col] / population.loc[col].iloc[-1]  # calculate cases per million
        except KeyError:
            pass
    return result