# Made by David van Eersel & Dominic Hildebrand
# June, 2021

from django.shortcuts import render
from utils import functions
genpanel = ""


def index(request):
    """Function renders home page & result page, based on web input
    Input: web request
    Return: Renders home.html
    OR
    Return: Renders results.html with results"""
    if request.method == 'POST':
        text_keywords = request.POST.get('text_keywords')
        text_gene_name = request.POST.get('text_gene_name')
        date_after = request.POST.get('date_after')
        text_exclude_genepanel = request.POST.get('text_exclude_genepanel')

        if text_gene_name is not None:
            parameter = {"keywords": text_keywords,
                         "gene_name": text_gene_name,
                         "date_after": date_after,
                         "exclude_genepanel": text_exclude_genepanel}
            results = functions.entrez_search(parameter, genpanel)
            return render(request, 'gtgp/results.html', {'results': results})
        elif text_gene_name is None:
            parameter = {"keywords": text_keywords,
                         "date_after": date_after,
                         "exclude_genepanel": text_exclude_genepanel}
            functions.entrez_search(parameter, genpanel)
            return render(request, 'gtgp/home.html')
        else:
            return render(request, 'gtgp/home.html')
    else:
        return render(request, 'gtgp/home.html')


def upload(request):
    """Function renders upload page, changes global genpanel
    Input: web request
    Return: renders webpage upload.html"""
    if request.method == "POST":
        global genpanel
        genpanel = request.POST.get("editor")
    return render(request, 'gtgp/upload.html')


def manual(request):
    """Function renders manual page
    Input: Web request
    Return: renders manual.html"""
    return render(request, 'gtgp/manual.html')


def about(request):
    """Function renders about page
    Input: Web request
    Return: renders about.html"""
    return render(request, 'gtgp/about.html')
