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


def upload_molprocessing(form):
        if form.vars.smiles:
            if is_valid_smiles(form.vars.smiles)==True:
                pass
            else: 
                form.errors.smiles = T('SMILES has an error, please check')
        else:
            form.errors.smiles = T('You must introduce an structure')  


#~ @auth.requires_membership('authorized')
def upload_compuesto():
    """
    action to upload compounds
    """
    form = SQLFORM(db.compound_record)
    if form.process(onvalidation=upload_molprocessing).accepted:
        name = form.vars.visitor_name
        molid = form.vars.id
        #update imagepath in db
        form.vars.imagepath = settings.imagedir+str(molid)+".png"
        row = db(db.compound_record.id==int(molid)).select().first()
        row.update_record(imagepath=form.vars.imagepath)
        descriptors = calculate_descriptors(form.vars.smiles)
        db.compound_descriptors.insert(   
            compound_record_id = molid,
            molecular_weight = descriptors["ExactMolWt"],
            tpsa = descriptors["TPSA"],
            num_rotatables_bonds = descriptors["NumRotatableBonds"],
            clogp = descriptors["MolLogP"],
            hbd = descriptors["NumHDonors"],
            hba = descriptors["NumHAcceptors"],
            )
        #create molecular image from smiles
        create_molimage(form.vars.smiles,form.vars.imagepath)
        response.flash = T("Compound was uploaded correctly")
        
    import urllib 
    from xml.dom import minidom 
    usock = urllib.urlopen('http://www.catalogueoflife.org/col/webservice?name=Carterina') 
    xmldoc = minidom.parse(usock)                              
    usock.close()                                              
    print xmldoc.toxml() 
        
    return dict(form=form)
    
@auth.requires_membership('authorized')
def upload_extracto():
    """
    action to upload compounds
    """
    form = SQLFORM(db.extract_record)
    if form.process().accepted:
        #~ name = form.vars.visitor_name
        #~ molid = form.vars.id
        response.flash = T("Compound was uploaded correctly")
    return dict(form=form)


