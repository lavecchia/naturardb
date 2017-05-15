# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
import os.path 


def buscar():
    """
    action to show a list of compounds
    """
    imagewidth = 70
    imageheight = 70
    request.is_local =False
    #extract of http://stackoverflow.com/questions/21447804/web2py-sqlform-grid-edit-page
    db.compound.id.readable = True
    db.compound.id.writeable = False
 

    form = SQLFORM.grid(
        query=db.compound,
        formname="compound",
        create=False,
        editable = auth.has_membership('managers'),
        deletable = auth.has_membership('managers'),
        buttons_placement = 'left',
        paginate = 5,
        #~ searchable= dict(cansmiles=True, synonym=True, extract=False),
        links=[dict(header=T('Image'), body = lambda row: 
        DIV(A(IMG(_src=URL('.',row.imagepath), 
        _width=imagewidth, _height=imageheight),_href=URL("buscar",args=["view/compound/%i"%(row.id)])),_class="img-zoom"))])
        
    if request.args(0):
        if "view" in request.args(0):
            compound_id = request.args(2)
            # Properties selection
            table = db(db.compoundproperty.compound_id==compound_id).select(
                db.compoundproperty.molecularweight,
                db.compoundproperty.molecularformula,
                #~ db.compoundproperty.molecular_volume,
                db.compoundproperty.logp,
                db.compoundproperty.tpsa,
                db.compoundproperty.hbd,
                db.compoundproperty.hba,
                db.compoundproperty.numrotatable,
                db.compoundproperty.numring,
                #~ db.compoundproperty.num_n,
                #~ db.compoundproperty.num_o,
                #~ db.compoundproperty.num_s,
                db.compoundproperty.numro5violation,
            )        
            properties = rows_transpose(table)
            
            # Docs selection
            docs_id = db(db.compound_doc.compound_id==compound_id).select(db.compound_doc.doc_id).as_list()
            print docs_id
            if docs_id!=[]:
                doclst = []
                for doc in docs_id:
                    table = db(db.doc.id==doc['doc_id']).select(
                        db.doc.journal,
                        db.doc.year,
                        db.doc.volume,
                        db.doc.issue,
                        db.doc.firstpage,
                        db.doc.lastpage,
                        db.doc.doi,
                        db.doc.isbn10,
                        db.doc.issn,
                        db.doc.pubmed_id,
                        db.doc.title,
                        db.doc.doctype,
                        db.doc.authors,
                        db.doc.abstract,
                        db.doc.url,
                        )
                    doclst.append(table.first())                    
            else:
                doclst = None
            
            # Molfile generation
            
            

    else:
        properties = ""
        doclst = None
        compound_id = ""
    
    
    #~ print doi2doc("10.1016/j.molstruc.2014.10.054")['message']['author']
   
    return dict(form=form, properties=properties, docs=doclst, compound_id=compound_id)
    

#get mol structure file wih compound_id
def get_mol():
    compound_id=request.args[0]
    filename="naturar_c%s.mol"%(compound_id)
    path=os.path.join(request.folder,'static/temp',filename)
    molfile = open(path,"w")
    response.headers['ContentType'] ="application/octet-stream";
    response.headers['Content-Disposition']="attachment; filename="+filename
    row = db(db.molstructure.compound_id==compound_id).select(db.molstructure.molstructure).first()
    try:
        molfile.write(row['molstructure'])
        molfile.close()
        return response.stream(open(path),chunk_size=4096)
    except:
        message = T("Problem in compound structure. Please report")
        return message 


    
    
