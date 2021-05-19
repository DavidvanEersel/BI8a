from Bio import Entrez
import requests


<<<<<<< HEAD
def entrezSearch(keywords="orchid",
                 genenames=["ABC", "ESR1"],
<<<<<<< HEAD
                 search_from="2020/06/12",
                 ):
    Entrez.email = "email"  # Misschien gebruiker om een email vragen?

    searchFrom = '2020/06/12'  # Must be YYYY/MM/DD OF YYYY/MM OF YYYY
    term = 'orchid'  # In Teams staat een advanced query voor een zoekterm
=======
                 searchFrom="2020/06/12",
                 ):
   
    boolAnd = True                                 # Misschien een boolean gebruiken voor de AND / OR statement? Anders opbouwen?

=======
def entrez_search(parameter):
>>>>>>> devbranch
    """Function searches PubMed for articles related to a search
    Input:  string keywords(str(term1 AND/OR term2))
            list genenames[gene1, gene2]
            string search_from(str date example(2020/06/12))
<<<<<<< HEAD
    Return: list[pmid's]"""

    Entrez.email = "sinbadisatwat@gmail.com"       # Misschien gebruiker om een email vragen?
    searchFrom = '2020/06/12'                      # Must be YYYY/MM/DD OF YYYY/MM OF YYYY
    term = 'orchid'                                # In Teams staat een advanced query voor een zoekterm

    # Moeten een manier zien te maken om AND / OR af anders te maken uit de website, anders
    if boolAnd == True:
        term = keywords
    if genenames != "":                            # Om af te vangen dat er geen 
        for gene in genenames:
            keywords += " AND " + gene
    if searchFrom == "":
        searchFrom = "1800/01/01"
     
    

    handle = Entrez.esearch(db="pubmed", term=term, mindate=searchFrom)
    res = Entrez.read(handle)
    Entrez.email = "email"    #Misschien gebruiker om een email vragen? 
    searchFrom = '2020/06/12' #Must be YYYY/MM/DD OF YYYY/MM OF YYYY
    term='orchid'             #In Teams staat een advanced query voor een zoekterm
>>>>>>> devbranch
    handle = Entrez.esearch(db="pubmed", term=term, mindate=searchFrom)
    res = Entrez.read(handle)
=======
    Return: list[pmid's]
    OR 
    Return: None if input is empty or null"""
    # Must be YYYY/MM/DD OF YYYY/MM OF YYYY
    # In Teams staat een advanced query voor een zoekterm
    # Misschien gebruiker om een email vragen?
    # https://www.ncbi.nlm.nih.gov/dbvar/content/tools/entrez/

    if parameter == "" or parameter is None:
        return None

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
    info = Entrez.esearch(db='pubmed', term=query)
    record = Entrez.read(info)
    count = record["Count"]
    print(count)
    info.close()
    handle = Entrez.esearch(db="pubmed", term=query, field="tiab", mindate=search_from, retmax=count)
    record = Entrez.read(handle)
>>>>>>> devbranch
    handle.close()

    list_ids = record['IdList']

<<<<<<< HEAD
    return list_ids
<<<<<<< HEAD

=======
    return pubtatorSearch(list_ids, count)
>>>>>>> devbranch

=======

<<<<<<< HEAD

>>>>>>> devbranch
def pubtatorSearch(list_ids):
    # TODO Maak vind een manier om met de NCBI link te werken
    # Voorbeelden pubtator search:
    # https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator?pmids=28483577&concepts=gene
    # https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids=PMC6207735
    # https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocjson?pmids=28483577,28483578,28483579
=======
def pubtatorSearch(list_ids, count):
    """Function uses PubTator API to textmine found hits. Hits get rudimentary score.
    Input:  list[str(pmid), str(pmid)]
    Return: Dict{key(str(pmid)) : tuple(str(score), str(pubtator_link), gennames[gene], diseases[disease], mutations[mutation])) Lists may be empty.
    OR
    Return: None if input is empty or null"""

    if list_ids == '' or list_ids == None:
        return None
>>>>>>> devbranch

    # Defaulting to gene, disease and mutation
    base_url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator?pmids={}&concepts=gene,disease,mutation"

<<<<<<< HEAD
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
<<<<<<< HEAD


pubtatorSearch(entrezSearch())
=======
>>>>>>> devbranch
=======
    articleLink = "https://www.ncbi.nlm.nih.gov/research/pubtator/?view=docsum&query=article"
    articleScore = 0
    gennames = []
    diseases = []
    mutations = []
    pmid = ""
    returnDict = {}
    for j in range(0, len(list_ids), 100):
        # Format IDs for PubTator
        string_ids = ""
        try:
            for i in range(100):
                string_ids += list_ids[j + i] + ','
        except IndexError:
            print("laatste aantal")
        # Remove last comma delimiter
        string_ids = string_ids[:-1]
        format_url = base_url.format(string_ids)

        # Get page details, var.text is important here
        res = requests.get(format_url)

        # Scores: Gene, mutation or disease in title:   +5 pts
        # Scores: Mutation or disease in abstract:      +2 pts
        # Scores: Gene in abstract                      +1 pt

        text = res.text.split("\n")
        for line in text:
            scored = False

            if '|t|' in line:
                titleLine = line.split('|t|')
                pmid = titleLine[0]
                title = titleLine[1]
                continue

            if '|a|' in line:
                continue

            if line != "":
                terms = line.split("\t")
                if int(terms[1]) < len(title):
                    articleScore += 5
                    scored = True
                if terms[4] == "Disease":
                    diseases = checkList(terms[3], diseases)
                    if not scored:
                        articleScore += 2
                elif terms[4] == "Mutation" or terms[4] == "DNAMutation" or terms[4] == "ProteinMutation" or terms[
                    4] == "SNP":
                    mutations = checkList(terms[3], mutations)
                    if not scored:
                        articleScore += 2
                elif terms[4] == "Gene":
                    gennames = checkList(terms[3], gennames)
                    if not scored:
                        articleScore += 1
                else:
                    print("A unexpected scoring error has occured for: " + terms[4])

            if line == "":
                articleLink = articleLink.replace("article", pmid)
                valueTuple = (gennames, diseases, mutations, articleLink, str(articleScore))
                if pmid != "":
                    returnDict[pmid] = valueTuple
                    pmid = ''
                articleLink = "https://www.ncbi.nlm.nih.gov/research/pubtator/?view=docsum&query=article"
                articleScore = 0
                gennames = []
                diseases = []
                mutations = []


    print("done")

    return returnDict


def checkList(var, varList):
    """Checks if variable is in list, if not, appends
    Input: str(var), varlist[var]
    Return: varlist[]"""
    if var not in varList:
        varList.append(var)
    return varList
>>>>>>> devbranch
