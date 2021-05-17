from Bio import Entrez
import requests


def entrezSearch(parameter):
    """Function searches PubMed for articles related to a search
    Input:  string keywords(str(term1 AND/OR term2))
            list genenames[gene1, gene2]
            string search_from(str date example(2020/06/12))
    Return: list[pmid's]
    OR 
    Return: None if input is empty or null"""
    # Must be YYYY/MM/DD OF YYYY/MM OF YYYY
    # In Teams staat een advanced query voor een zoekterm
    # Misschien gebruiker om een email vragen?
    # https://www.ncbi.nlm.nih.gov/dbvar/content/tools/entrez/
    
    if parameter == "" or parameter == None:
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
    handle = Entrez.esearch(db="pubmed", term=query, field="tiab", mindate=search_from)
    record = Entrez.read(handle)
    handle.close()

    list_ids = record['IdList']
    pubtatorSearch(list_ids)


def pubtatorSearch(list_ids):
    """Function uses PubTator API to textmine found hits. Hits get rudimentary score.
    Input:  list[str(pmid), str(pmid)]
    Return: Dict{key(str(pmid)) : tuple(str(score), str(pubtator_link), gennames[gene], diseases[disease], mutations[mutation])) Lists may be empty.
    OR
    Return: None if input is empty or null"""
    
    if list_ids == '' or list_ids == None:
        return None

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

    # Scores: Gene, mutation or disease in title:   +5 pts
    # Scores: Mutation or disease in abstract:      +2 pts
    # Scores: Gene in abstract                      +1 pt
    titleLine = ""
    scored = False
    articleLink = "https://www.ncbi.nlm.nih.gov/research/pubtator/?view=docsum&query=article"
    articleScore = 0
    gennames = []
    diseases = []
    mutations = []
    returnDict = {}
    text = res.text.split("\n")
    
    for line in text:

        if '|t|' in line:
            titleLine = line.split('|t|')
            pmid = titleLine[0]
            title = titleLine[1]
            continue
        
        if '|a|' in line:
            continue

        
        if line != "":
            # print(line.split("\t"))
            terms = line.split("\t")
            if int(terms[1]) < len(title):
                articleScore += 5
                scored = True
            if terms[4] == "Disease":
                diseases = checkList(terms[3], diseases)
                if scored == False:
                    articleScore += 2
            elif terms[4] == "Mutation":
                mutations = checkList(terms[3], mutations)
                if scored == False: 
                    articleScore += 2
            elif terms[4] == "Gene":
                gennames = checkList(terms[3], gennames)
                if scored == False: 
                    articleScore += 1
            else:
                print("A unexpected scoring error has occured for: "+ terms[4])

        if line == "":
            
            # Dict{key(str(pmid)) : tuple(str(articleScore), str(articleLink), gennames[gene], diseases[disease], mutations[mutation])) Lists may be empty.
            articleLink = articleLink.replace("article", pmid)        
            valueTuple = (str(articleScore), articleLink, gennames, diseases, mutations)
            returnDict[pmid] = valueTuple
            titleLine = ""
            scored = False
            articleLink = "https://www.ncbi.nlm.nih.gov/research/pubtator/?view=docsum&query=article"
            articleScore = 0
            gennames = []
            diseases = []
            mutations = []

    return returnDict

def checkList(var, varList):
    """Checks if variable is in list, if not, appends
    Input: str(var), varlist[var]
    Return: varlist[]"""
    if var not in varList:
        varList.append(var)
    return varList