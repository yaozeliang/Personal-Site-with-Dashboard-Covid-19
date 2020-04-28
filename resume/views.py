from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class ResumeView(TemplateView):
    template_name='resume/resume.html'