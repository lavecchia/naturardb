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

#~ def list_molecules():
    #~ """
    #~ show compound like a image grid
    #~ """
    #~ if len(request.args): page=int(request.args[0])
    #~ else: page=0
    #~ items_per_page=5
    #~ limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #~ rows=db().select(db.compound_record.ALL,limitby=limitby)
    #~ return dict(rows=rows,page=page,items_per_page=items_per_page)


#~ def list_molecules2():
    #~ grid = SQLFORM.smartgrid(db.compound_record, paginate=5)
    #~ return locals()


def listar():
    """
    action to show a list of compounds
    """
    request.is_local =False
    #extract of http://stackoverflow.com/questions/21447804/web2py-sqlform-grid-edit-page
    db.compound_record.id.readable = False
    db.compound_record.id.writeable = False

    form = SQLFORM.grid(query=db.compound_record, 
        paginate = 5,
    links=[dict(header=T('Image'), body = lambda row: 
        A(IMG(_src=URL('static',row.imagepath), 
        _width=70, _height=70)))])

    return dict(form=form)


