import requests
from Bio import Entrez


def entrez_search(parameter, genpanel):
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
    genpanel_symbol, genpanel = read_genpanel(genpanel)
    keywords = parameter["keywords"]
    genenames = parameter["gene_name"]
    search_from = parameter["date_after"].replace("-", "/")

    keyword = query_builder(keywords)
    genename = query_builder(genenames)

    if genename == "":
        query = keyword
    elif keyword == "":
        query = genename
    elif genename != "" and keyword == "":
        query = keyword + " AND " + genename
    else:
        return None

    if search_from == "":
        search_from = "1800/01/01"
    query = query + "({}[Date - Publication]:3000/12/31[Date - Publication)".format(search_from)

    Entrez.email = "sinbadisatwat@gmail.com"
    info = Entrez.esearch(db='pubmed', field='tiab', term=query)
    record = Entrez.read(info)
    count = record["Count"]
    info.close()

    handle = Entrez.esearch(db="pubmed", term=query, field="tiab", retmax=count)
    record = Entrez.read(handle)
    handle.close()

    list_ids = record['IdList']
    if genename != "":
        return pubtatorSearch(list_ids, count, genename, keywords)
    else:
        return pubtatorSearch(list_ids, count, "", keywords)


def query_builder(search):
    query = ""
    or_ = False
    for i in search:
        if i == '(':
            i = "("
            or_ = True
        if i == ')':
            or_ = False
            i = ")"
        if i == ";":
            if or_ is True:
                i = " OR "
            else:
                i = " AND "
        query = query + i
    return query


def pubtatorSearch(list_ids, count, genename, keywords):
    """Function uses PubTator API to textmine found hits. Hits get rudimentary score.
    Input:  list[str(pmid), str(pmid)]
    Return: Dict{key(str(pmid)) : tuple(gennames, diseases, mutations, articleLink, str(articleScore)) Lists may be empty.
    OR
    Return: None if input is empty or null"""

    if list_ids == '' or list_ids is None:
        return None

    keywords = keywords.replace("(", "")
    keywords = keywords.replace(")", "")
    keywords = keywords.lower()
    keywords = keywords.split(";")

    # Defaulting to gene, disease and mutation
    base_url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator?pmids={}&concepts=gene,disease,mutation"

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
                    if terms[1].lower() in keywords:
                        articleScore += 5
                        scored = True
                if terms[4] == "Disease":
                    diseases = checkList(terms[3], diseases)
                    if not scored:
                        if terms[3].lower() in keywords:
                            articleScore += 2
                elif terms[4] == "Mutation" or terms[4] == "DNAMutation" or terms[4] == "ProteinMutation" or terms[
                    4] == "SNP":
                    mutations = checkList(terms[3], mutations)
                    if not scored:
                        if terms[3].lower() in keywords:
                            articleScore += 2
                elif terms[4] == "Gene":
                    gennames = checkList(terms[3], gennames)
                    if not scored:
                        if terms[3].lower() in keywords:
                            articleScore += 1
                else:
                    print("A unexpected scoring error has occured for: " + terms[4])

            if line == "":
                articleLink = articleLink.replace("article", pmid)
                valueTuple = (gennames, diseases, mutations, articleLink, str(articleScore))
                if pmid != "" and int(articleScore) > 0:
                    if genename != "":
                        if genename in valueTuple:
                            returnDict[pmid] = valueTuple
                            pmid = ''
                    else:
                        returnDict[pmid] = valueTuple
                        pmid = ''
                articleLink = "https://www.ncbi.nlm.nih.gov/research/pubtator/?view=docsum&query=article"
                articleScore = 0
                gennames = []
                diseases = []
                mutations = []


    returnDict = dict(sorted(returnDict.items(), key=lambda item: int(item[1][4]), reverse=True))
    return returnDict


def checkList(var, varList):
    """Checks if variable is in list, if not, appends
    Input: str(var), varlist[var]
    Return: varlist[]"""
    if var not in varList:
        varList.append(var)
    return varList


def read_genpanel(g):
    x = str(g).split('\n')
    genpanel_symbol = []
    genpanel = []
    index_genpanel_symbol = 0
    index_genpanel = 0

    for i in range(len(x)):
        temp = x[i].split('\t')
        for j in range(len(temp)):
            if temp[j] == "GenePanels_Symbol":
                index_genpanel_symbol = j
                print(j)
            if temp[j] == "GenePanel":
                index_genpanel = j
                print(j)
            if temp != ['']:
                genpanel_symbol.append(temp[index_genpanel_symbol])
                genpanel.append(temp[index_genpanel])

    return genpanel_symbol, genpanel
