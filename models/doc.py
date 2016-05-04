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
    return data
    

def isbn2doc(isbn):
    url = "http://isbndb.com/api/v2/json/VAKSOIXR/book/" + isbn
    response = urllib.urlopen(url)
    data = json.load(response)
    return data


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
    
    

    
         
       


