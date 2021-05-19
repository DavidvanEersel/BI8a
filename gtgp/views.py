from django.shortcuts import render
from utils import functions


def index(request):
    if request.method == 'POST':
        text_keywords = request.POST.get('text_keywords')
        text_gene_name = request.POST.get('text_gene_name')
        date_after = request.POST.get('date_after')
        text_exclude_genepanel = request.POST.get('text_exclude_genepanel')
        # TODO gene_name = none dan zoek je naar NIEUWE GENEN
        # TODO gene_name != none dan zoek je naar NIEUWE INFO OVER DE GENEN

        if text_gene_name is not None:
            parameter = {"keywords": text_keywords,
                         "gene_name": text_gene_name,
                         "date_after": date_after,
                         "exclude_genepanel": text_exclude_genepanel}
            results = functions.entrez_search(parameter)
            results = function.sort_results(results)

            return render(request, 'gtgp/results.html', {'results':results})

        elif text_gene_name is None:
            parameter = {"keywords": text_keywords,
                         "date_after": date_after,
                         "exclude_genepanel": text_exclude_genepanel}
            functions.entrez_search(parameter)
            return render(request, 'gtgp/home.html')
        else:
            return render(request, 'gtgp/home.html')
    else:
        return render(request, 'gtgp/home.html')


def upload(request):
    if request.method == "POST":
        test = request.POST.get("file_upload")
        print(test)
    return render(request, 'gtgp/upload.html')


def manual(request):
    return render(request, 'gtgp/manual.html')


def about(request):
    return render(request, 'gtgp/about.html')
# Create your views here.
