from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def Index(req):
    return render(req, 'index.html')
