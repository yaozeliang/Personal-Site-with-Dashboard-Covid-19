import pandas as pd
import requests
import numpy as np
from datetime import datetime

base_url ="https://api.covid19api.com/"
summary_url = base_url+"summary"
country_url = base_url+"countries"


def get_global_data():
    summary_r = requests.get(summary_url)
    global_data = summary_r.json()['Global']
    return global_data


def get_all_country_data():
    summary_r = requests.get(summary_url)
    all_countries = summary_r.json()['Countries']
    country_data = {
    'Country':[],
    'CountryCode':[],
    'NewConfirmed':[],
    'TotalConfirmed':[],
    'NewDeaths':[],
    'TotalDeaths':[],
    'NewRecovered':[],
    'TotalRecovered':[],
    'Date':[],
    
}
    for ele in all_countries:
        for k,v in country_data.items():
            v.append(ele[k])

    df_country = pd.DataFrame(country_data)
    df_country['Date'] = df_country['Date'].apply(lambda x:x.split('T')[0])
    df_country = df_country.sort_values(by=['TotalConfirmed'], ascending = False)

    return df_country


def get_country_last_n_days(countryname,num_days):

    url = f"https://api.covid19api.com/total/country/{countryname}/status/confirmed"
    r = requests.get(url)
    df =pd.DataFrame(r.json()).tail(num_days)
    df.loc[:,'Date'] = df['Date'].apply(lambda x:x.split('T')[0])
    df = df.loc[:,['Country','Date','Cases']]

    return df


