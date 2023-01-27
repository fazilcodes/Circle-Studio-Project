from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def Index(req):
    return render(req, 'index.html')


def Signin(req):
    return render(req, 'login1.html')


def Signup(req):
    return render(req, 'login.html')
