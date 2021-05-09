from django.shortcuts import render

from utils import test

def index(request):
    print(test.main())
    return render(request, 'gtgp/templates/home.html')

def upload(request):
    return render(request, 'gtgp/upload.html')

# Create your views here.
