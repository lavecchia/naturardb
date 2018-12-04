# DOC functions (bibliography)
#
import urllib, json
from datetime import datetime

'''
Import DOC information from DOI using CrossRef Api
'''
def doi2doc(doi):
    url = "http://api.crossref.org/works/" + doi
    try:
        response = urllib.urlopen(url)
        data = json.load(response)
    except:
        pass
    doc = {}
    try:
        doc['journal']=data['message']['container-title'][0]
    except:
        doc['journal']="-"
        
    try:
        doc['year']=datetime.strptime(str(data['message']['deposited']['date-parts'][0][0]), '%Y')
    except:
        doc['year']=0000
        
    try:
        doc['volume']=data['message']['volume']
    except:
        doc['volume']=0
        
    try:
        doc['issue']=data['message']['issue']
    except:
        doc['issue']=0
        
    try:
        pages = data['message']['page'].split("-")
        doc['firstpage']=pages[0]
        doc['lastpage']=pages[1]
    except:
        doc['firstpage']=0
        doc['lastpage']=0
    
    try:           
        doc['doi']=data['message']['DOI']
    except:
        doc['doi']=doi
    
    try:
        doc['issn']=data['message']['ISSN']
    except:
        doc['issn']="0"
        
    #~ Field('pubmed_id'),
    try:
        doc['title']=data['message']['title'][0]    
    except:
        doc['title']="-"
    
    try:
        doc['doctype']=data['message']['type']
    except:
        doc['doctype']="-"
    
    try:
        authorlst= []
        for iauthor in data['message']['author']:
            authorlst.append(iauthor['given'] + " " + iauthor['family'])
        doc['authors']=",".join(authorlst)
    except:
        doc['authors']="-"
        
    
    #~ Field('abstract', type='text'),
    try:
        doc['url']=data['message']['URL']
    except:
        doc['url']="-"
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
    
    

    
         
       


