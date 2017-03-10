# DOC functions (bibliography)
#
import urllib, json

'''
Import DOC information from DOI using CrossRef Api
'''
def doi2doc(doi):
    url = "http://api.crossref.org/works/" + doi
    response = urllib.urlopen(url)
    data = json.load(response)
    doc = {}
    doc['journal']=data['message']['container-title'][0]
    doc['year']=data['message']['deposited']['date-parts'][0][0]
    doc['volume']=data['message']['volume']
    doc['issue']=data['message']['issue']
    
    pages = data['message']['page'].split("-")
    doc['firstpage']=pages[0]
    doc['lastpage']=pages[1]
    
    doc['doi']=data['message']['DOI']
    doc['issn']=data['message']['ISSN']
    #~ Field('pubmed_id'),
    doc['title']=data['message']['title'][0]    
    doc['doctype']=data['message']['type']
    
    authorlst= []
    for iauthor in data['message']['author']:
        authorlst.append(iauthor['given'] + " " + iauthor['family'])
    doc['authors']=",".join(authorlst)
    
    #~ Field('abstract', type='text'),
    doc['url']=data['message']['URL']
    return doc
    

def isbn2doc(isbn):
    url = "http://isbndb.com/api/v2/json/VAKSOIXR/book/" + isbn
    response = urllib.urlopen(url)
    data = json.load(response)
    doc={}
    doc['journal']=""
    doc['year']=""
    doc['volume']=""
    doc['issue']=""
    
    pages = ""
    doc['firstpage']=""
    doc['lastpage']=""
    
    doc['doi']=""
    doc['issn']=data['data']['isbn13']
    #~ Field('pubmed_id'),
    doc['title']=data['data']['title']  
    doc['doctype']="book"
    
    authorlst= []
    for iauthor in data['data']['author_data']:
        authorlst.append(iauthor['name'])
    doc['authors']=",".join(authorlst)
    
    #~ Field('abstract', type='text'),
    doc['url']=""
    return doc


'''
Detect if string is a DOI, URL, ISBN or complete reference
'''
def input2doc(referencia):
    referenciastrip = referencia.replace("-",'').replace(" ",'')
    # DOI
    if referencia.startswith( '10.' ):
        return doi2doc(referencia)
    # ISBN13
    elif (len(referenciastrip)==13) and (referenciastrip.startswith('978') or referenciastrip.startswith('979')):
        return isbn2doc(referenciastrip)
    # ISBN10
    elif len(referenciastrip)==10:
        return isbn2doc(referenciastrip)
    # URL
    elif ('www' in referencia) or ('http' in referencia) or ('.com' in referencia) or ('.edu' in referencia):
        return {'url':referencia}
    
    

    
         
       


