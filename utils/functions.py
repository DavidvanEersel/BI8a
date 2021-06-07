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
    genpanel_symbol, genpanel, genepanel_names = read_genpanel(genpanel)
    keywords = parameter["keywords"]
    genenames = parameter["gene_name"]
    search_from = parameter["date_after"].replace("-", "/")

    query = query_builder(keywords)
    genename = query_builder(genenames)

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
        return pubtatorSearch(list_ids, genename, keywords, genpanel_symbol, genpanel, genepanel_names)
    else:
        return pubtatorSearch(list_ids, "", keywords, genpanel_symbol, genpanel, genepanel_names)


def query_builder(search):
    """ Creates query accepted by EntrezSearch using keywords from webpage
    Input: search str(content of keywords from webpage, example: 
                                    (deaf;deafness;hearingloss);(ATP;ADP;AMP;cAMP;cyclicAMP);
    Return: query str(query accepted by EntrezSearch)"""
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


def pubtatorSearch(list_ids, genename, keywords, genpanel_symbol, genpanel, genepanel_names):
    """ 
    Function uses PubTator API to textmine found hits. Hits get rudimentary score. 
    Calls functions "split_keywords()" and "score_Generator()"
    
    Input:              list_ids: [str(pmid), 
        genename:           str("single gene") #Genename submitted in gene names on website,
        keywords:           str((deaf;deafness;hearingloss);(ATP;ADP;AMP;cAMP;cyclicAMP);) example keywords from webpage,
        genpanel_symbol:    list[genpanel symbols]
        genpanel:           list[genpanel] table in which genepanel symbols are in
        genpanel_names      list[Symbol HGNC + Alias] table in from GenePanel
    
    Return: Dict{key(str(pmid)) : tuple(gennames[], diseases[], mutations[], str(articleLink), str(articleScore), str(genpanel)) Lists may be empty.
    OR
    Return: None if input is empty or null"""

    # If input empty, stop function.
    if list_ids == '' or list_ids is None:
        return None

    # Default URL & variables
    base_url = "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator?pmids={}&concepts=gene,disease,mutation"
    articleLink = "https://www.ncbi.nlm.nih.gov/research/pubtator/?view=docsum&query=article"
    keywords = split_keywords(keywords)
    articleScore = 0
    gennames = []
    diseases = []
    mutations = []
    pmid = ""
    returnDict = {}
    title = ""

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

        text = res.text.split("\n")
        for line in text:

            if '|t|' in line:
                titleLine = line.split('|t|')
                pmid = titleLine[0]
                title = titleLine[1]
                continue

            elif '|a|' in line:
                continue

            elif line != "":
                articleScore, gennames, mutations, diseases = score_Generator(line, title, articleScore, keywords,
                                                                              gennames, mutations, diseases)


            elif line == "":
                if pmid != "" and int(articleScore) > 0:
                    if genename != "":
                        for gen in gennames:
                            if gen.lower() == genename.lower():
                                for keys, values in genepanel_names.items():
                                    if genename in values:
                                        valueTuple = (
                                            gennames, diseases, mutations, articleLink, str(articleScore), keys)
                                        returnDict[pmid] = valueTuple
                                        pmid = ''

                    else:
                        for gen in gennames:
                            for keys, values in genepanel_names.items():
                                if gen in values:
                                    valueTuple = (
                                        gennames, diseases, mutations, articleLink, str(articleScore), keys)
                                    returnDict[pmid] = valueTuple
                                    pmid = ''
                                else:
                                    valueTuple = (
                                        gennames, diseases, mutations, articleLink, str(articleScore))
                                    returnDict[pmid] = valueTuple
                                    pmid = ''

                articleLink = "https://www.ncbi.nlm.nih.gov/research/pubtator/?view=docsum&query=article"
                articleScore = 0
                gennames = []
                diseases = []
                mutations = []
    returnDict = dict(sorted(returnDict.items(), key=lambda item: int(item[1][4]), reverse=True))
    return returnDict


def split_keywords(keywords):
    """ Function to split keywords and return a list of keywords for scoring
    Input:      keywords str('(deaf;deafness;hearingloss);(ATP;ADP;AMP;cAMP;cyclicAMP);')
    Return:     keywords list['deaf','deafness','hearingloss','ATP','ADP','AMP','cAMP','cyclicAMP']   
    """
    keywords = keywords.replace("(", "")
    keywords = keywords.replace(")", "")
    keywords = keywords.lower()
    keywords = keywords.split(";")
    return keywords


def score_Generator(line, title, articleScore, keywords, gennames, mutations, diseases):
    """Used by pubtatorSearch function to generate a score.
    Input: 
        line            str() pubtator format line, 
        title           str() pubtator format title line, 
        articleScore    int(numer) score for the article, 
        keywords        list[] of keywords used to search, 
        gennames        list[] of gennames found in the article, 
        mutations       list[] of mutations found in the article, 
        diseases        list[] of diseases found in the article,
    Return:
        articleScore    int(numer) score for the article, 
        gennames        list[] of gennames found in the article, 
        mutations       list[] of mutations found in the article, 
        diseases        list[] of diseases found in the article,
    """
    # Scores: Gene, mutation or disease in title:   +5 pts
    # Scores: Mutation or disease in abstract:      +2 pts
    # Scores: Gene in abstract                      +1 pt

    scored = False
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

    return articleScore, gennames, mutations, diseases


def checkList(var, varList):
    """Checks if variable is in list, if not, appends
    Input: str(var), varlist[var]
    Return: varlist[]"""
    if var not in varList:
        varList.append(var)
    return varList


def read_genpanel(g):
    """ Reads useful data from Genpanel file contents
    Input: g        str(content of upload page textbox)
    Return: 
    genpanel_symbol list[genpanel symbols] contents from genpanel tsv, 
    genpanel        list[genpanel ] contents from genpanel tsv, 
    symbol_HGNC     list[symbol_HGNC] contents from genpanel tsv"""
    x = str(g).split('\n')
    genpanel_symbol = []
    genpanel = []
    symbol_HGNC = []
    aliases = []

    index_genpanel_symbol = 0
    index_genpanel = 0
    index_aliases = 0
    index_symbol_HGNC = 0

    dict ={}

    # Gather required data from GenPanel
    for i in range(len(x)):
        temp = x[i].split('\t')
        for j in range(len(temp)):
            if temp[j] == "GenePanel":
                index_genpanel = j
            if temp[j] == "Symbol_HGNC":
                index_symbol_HGNC = j
            if temp[j] == "Aliases":
                index_aliases = j
            if temp != ['']:
                dict[temp[index_genpanel]] = [temp[index_symbol_HGNC]] +  temp[index_aliases].split("|")

    return genpanel_symbol, genpanel, dict
