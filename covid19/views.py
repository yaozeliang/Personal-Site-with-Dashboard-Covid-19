from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
import numpy as np
import pandas as pd
from .source import get_all_country_data,get_global_data,get_country_last_n_days
import datetime
import json

today_date = datetime.datetime.now().strftime("%Y-%m-%d")
col_top_10_today = ['Country','NewConfirmed','NewDeaths','NewRecovered','Date']
col_top_10_total = ['Country','TotalConfirmed','TotalDeaths','TotalRecovered']

# fr_five_days = get_country_last_n_days('france',5)
# fr_last_date=list(fr_five_days['Date'])
# fr_last_confirmed=list(fr_five_days['Cases'])

fr_five_days = get_country_last_n_days('France',5)
england_five_days = get_country_last_n_days('GB',5)
spain_five_days = get_country_last_n_days('ES',5)
italy_five_days = get_country_last_n_days('IT',5)
germany_five_days = get_country_last_n_days('DE',5)

def home(request):
    general_data= get_global_data()
    total= get_all_country_data().get('total')
    today = get_all_country_data().get('today')

    top_ten_today = today.loc[:,col_top_10_today]
    top_ten_total= total.loc[:,col_top_10_total]

    
    fr_5_date=list(fr_five_days['Date'])

    fr_5_confirmed=list(fr_five_days['Cases'])
    en_5_confirmed=list(england_five_days['Cases'])
    sp_5_confirmed=list(spain_five_days['Cases'])
    it_5_confirmed=list(italy_five_days['Cases'])
    ger_5_confirmed=list(germany_five_days['Cases'])

    top_10_coutnrys_total=list(top_ten_total['Country'])
    top_10_confirm_total=list(top_ten_total['TotalConfirmed'])
    top_10_death_total = list(top_ten_total['TotalDeaths'])
    top_10_recover_total = list(top_ten_total['TotalRecovered'])

    top_10_coutnrys_today=list(top_ten_today['Country'])
    top_10_confirm_today=list(top_ten_today['NewConfirmed'])
    top_10_death_today = list(top_ten_today['NewDeaths'])
    top_10_recover_today = list(top_ten_today['NewRecovered'])


    context={'general_data':general_data,
             'top_ten_today': top_ten_today,
             'top_ten_total':top_ten_total,
             'today_date':today_date,
             'fr_5_date':json.dumps(fr_5_date),
             'fr_5_confirmed':json.dumps(fr_5_confirmed),
             'en_5_confirmed':json.dumps(en_5_confirmed),
             'sp_5_confirmed':json.dumps(sp_5_confirmed),
             'it_5_confirmed':json.dumps(it_5_confirmed),
             'ger_5_confirmed':json.dumps(ger_5_confirmed),
             'top_10_coutnrys_total':json.dumps(top_10_coutnrys_total),
             'top_10_confirm_total':json.dumps(top_10_confirm_total),
             'top_10_death_total':json.dumps(top_10_death_total),
             'top_10_recover_total':json.dumps(top_10_recover_total),
             'top_10_coutnrys_today':json.dumps(top_10_coutnrys_today),
             'top_10_confirm_today':json.dumps(top_10_confirm_today),
             'top_10_death_today':json.dumps(top_10_death_today),
             'top_10_recover_today':json.dumps(top_10_recover_today),
             }
    return render(request, 'covid19/general.html',context)