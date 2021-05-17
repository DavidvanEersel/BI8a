from Bio import Entrez
import requests


def entrezSearch(parameter):
    """Function searches PubMed for articles related to a search
       Input:  string keywords(str(term1 AND/OR term2))
               list genenames[gene1, gene2]
               string search_from(str date example(2020/06/12))
       Return: list[pmid's]"""
    # Must be YYYY/MM/DD OF YYYY/MM OF YYYY
    # In Teams staat een advanced query voor een zoekterm
    # Moeten een manier zien te maken om AND / OR af anders te maken uit de website, anders
    # Misschien gebruiker om een email vragen?
    # https://www.ncbi.nlm.nih.gov/dbvar/content/tools/entrez/
    keywords = parameter["keywords"]
    search_from = parameter["date_after"]
    query = ""
    or_ = False
    for i in keywords:
        if i == '(':
            i = "("
            or_ = True
        else:
            quote = True
        if i == ')':
            or_ = False
            i = ")"
        else:
            quote = True
        if i == ";":
            if or_ is True:
                i = " OR "
            else:
                i = " AND "
        query = query + i

    if search_from == "":
        search_from = "1800/01/01"

    Entrez.email = "sinbadisatwat@gmail.com"
    handle = Entrez.esearch(db="pubmed", term=query, field="tiab", mindate=search_from)
    record = Entrez.read(handle)
    handle.close()

    list_ids = record['IdList']
    pubtatorSearch(list_ids)


def pubtatorSearch(list_ids):
    # TODO Maak vind een manier om met de NCBI link te werken
    # Voorbeelden pubtator search:
    # https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator?pmids=28483577&concepts=gene
    # https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids=PMC6207735
    # https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmids=28483577,28483578,28483579

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
