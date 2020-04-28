from django.urls import path,include
from . import views


app_name='resume'

urlpatterns = [
    path("",views.ResumeView.as_view(),name='resume')
]