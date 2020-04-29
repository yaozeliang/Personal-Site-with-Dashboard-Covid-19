from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
import numpy as np
import pandas as pd
from .source import get_all_country_data,get_global_data,get_country_last_n_days
import datetime


today = datetime.datetime.now().strftime("%Y-%m-%d")
col_top_10_today = ['Country','NewConfirmed','NewDeaths','NewRecovered','Date']
col_top_10_total = ['Country','TotalConfirmed','TotalDeaths','TotalRecovered']


fr_five_days = get_country_last_n_days('France',5)
fr_last_date=list(fr_five_days['Date'])
fr_last_confirmed=list(fr_five_days['Cases'])




def home(request):
    general_data= get_global_data()
    all_country_data= get_all_country_data()
    top_ten_today = all_country_data.loc[:,col_top_10_today].head(10)
    top_ten_total= all_country_data.loc[:,col_top_10_total].head(10)

    fr_last_date=list(fr_five_days['Date'])
    fr_last_confirmed=list(fr_five_days['Cases'])

    context={'general_data':general_data,
             'top_ten_today': top_ten_today,
             'top_ten_total':top_ten_total,
             'today':today,
             'fr_last_date':fr_last_date,
             'fr_last_confirmed':fr_last_confirmed}
    return render(request, 'covid19/general.html',context)