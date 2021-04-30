from Bio import entrez 

def entrezSearch():
    idList = []

    Entrez.email = "email"    #Misschien gebruiker om een email vragen? 
    searchFrom = '2020/06/12' #Must be YYYY/MM/DD OF YYYY/MM OF YYYY
    term='orchid'             #In Teams staat een advanced query voor een zoekterm
    handle = entrez.esearch(db="pubmed", term=term, mindate=searchFrom)
    record = entrez.read(handle)
    handle.close()
    for id in record:
        print(id['idList'])
    #TODO Maak hier een lijst van zodat je een lijst met PubMed ID's hebt voor een pubtator search

    return idList

def pubtatorSearch(idList):
    #TODO Maak vind een manier om met de NCBI link te werken
    #Voorbeelden pubtator search:
    # https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator?pmids=28483577&concepts=gene
    # https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids=PMC6207735
    # https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmids=28483577,28483578,28483579
    # Leren format pubtator format lezen

    return None
    