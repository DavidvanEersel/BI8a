from Bio import Entrez
import requests


def entrezSearch(keywords="orchid",
                 genenames=["ABC", "ESR1"],
                 search_from="2020/06/12",
                 ):
    Entrez.email = "email"  # Misschien gebruiker om een email vragen?

    searchFrom = '2020/06/12'  # Must be YYYY/MM/DD OF YYYY/MM OF YYYY
    term = 'orchid'  # In Teams staat een advanced query voor een zoekterm
    handle = Entrez.esearch(db="pubmed", term=term, mindate=searchFrom)
    res = Entrez.read(handle)
    handle.close()

    # https://www.ncbi.nlm.nih.gov/dbvar/content/tools/entrez/
    list_ids = res['IdList']

    return list_ids


def pubtatorSearch(list_ids):
    # TODO Maak vind een manier om met de NCBI link te werken
    # Voorbeelden pubtator search:
    # https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator?pmids=28483577&concepts=gene
    # https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids=PMC6207735
    # https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmids=28483577,28483578,28483579
    # Leren format pubtator format lezen

    # Defaulting to gene, disease and mutation
    base_url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator?pmids={}&concepts=gene,disease,mutation"

    # Format IDs for PubTator
    string_ids = ""
    for pmcid in list_ids:
        string_ids += pmcid + ','

    # Remove last comma delimiter
    string_ids = string_ids[:-1]
    format_url = base_url.format(string_ids)

    # Get page details, var.text is important here
    res = requests.get(format_url)

    text = res.text.split("\n")
    for line in text:
        if line:
            print("Line")
        else:
            print("Next")

    return None


pubtatorSearch(entrezSearch())
