from django.shortcuts import render

from utils import test

def index(request):
    print(test.main())
    return render(request, 'gtgp/home.html')

def upload(request):
    return render(request, 'gtgp/upload.html')

def manual(request):
    return render(request, 'gtgp/manual.html')
# Create your views here.
