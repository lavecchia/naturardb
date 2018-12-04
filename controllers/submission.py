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
from os import rename
from time import sleep

def synonymlist(row):
    synonyms = db((db.tmpsynonym.compoundsubmission_id == row.compoundsubmission.id)).select()
    return ', '.join(synonym.synonymname for synonym in synonyms)
    

@auth.requires_membership('managers')
def compound_to_approve():
    """
    action to show a list of compounds
    """
    imagewidth = 70
    imageheight = 70
    #~ db.compoundsubmission.synonym = Field.Virtual('synonym', synonymlist)
    db.compoundsubmission.created_on.readable = True
    query = db(db.compoundsubmission.approved==False)
    form = SQLFORM.grid(query,create=False,editable=False,deletable=True,     
    links=[dict(header=T('Image'), body = lambda row: CAT(DIV(IMG(_src=URL('.',row.imagepath), _width=imagewidth, _height=imageheight),_class="img-zoom")," ", A('Aprobar',_href=URL("submission","compound_approval",args=[row.id]))))],        
    paginate=10,
        fields=[db.compoundsubmission.id , db.compoundsubmission.created_on, db.compoundsubmission.created_by, db.compoundsubmission.inputsmiles,db.compoundsubmission.synonym,db.compoundsubmission.source,db.compoundsubmission.imagepath ])
    
    
    if request.args(0):
        if "view" in request.args(0) or "edit" in request.args(0):
            compound_id = request.args(2)
             # Docs selection
            docs_id = db(db.doctmp.compoundsubmission_id==compound_id).select(db.doctmp.id).as_list()
            print docs_id
            if docs_id!=[]:
                doclst = []
                for doc in docs_id:
                    table = db(db.doctmp.id==doc['id']).select(
                        db.doctmp.journal,
                        db.doctmp.year,
                        db.doctmp.volume,
                        db.doctmp.issue,
                        db.doctmp.firstpage,
                        db.doctmp.lastpage,
                        db.doctmp.doi,
                        db.doctmp.isbn10,
                        db.doctmp.issn,
                        db.doctmp.pubmed_id,
                        db.doctmp.title,
                        db.doctmp.doctype,
                        db.doctmp.authors,
                        db.doctmp.abstract,
                        db.doctmp.url,
                        )
                    doclst.append(table.first())                    
            else:
                doclst = None
            
            # Molfile generation
            
            

    else:
        doclst = None
        compound_id = ""
    
    properties = ""

    #~ print doi2doc("10.1016/j.molstruc.2014.10.054")['message']['author']
   
    return dict(form=form, docs=doclst, properties=properties, compound_id=compound_id)       
        

@auth.requires_membership('managers')
def compound_approval():
    tmpcompoundid = request.args(0, cast=int)
    tmpcompound = db.compoundsubmission(id=tmpcompoundid) or redirect(URL('index'))
    
    if tmpcompound['approved'] == False:
        #insert new compound
        compound_id = db.compound.insert(inchi=tmpcompound['inchi'],
        inchikey=tmpcompound['inchikey'],
        isosmiles=tmpcompound['isosmiles'],
        cansmiles=tmpcompound['cansmiles'],
        addinfo=tmpcompound['addinfo'],
        synonym=tmpcompound['synonym'],
        semisynthetic=tmpcompound['semisynthetic'],
        structuraluncertainty=tmpcompound['structuraluncertainty'],
        created_by=tmpcompound['created_by'],
        source=tmpcompound['source'],
        )
        print compound_id
        #change image file name and imagepath
        imagepath = tmpcompound['imagepath'].replace("tmp%i"%tmpcompoundid, str(compound_id))
        db(db.compound.id == compound_id).update(imagepath=imagepath)
        #~ print os.path.join(request.folder,tmpcompound['imagepath'])
        #~ print imagepath
        try:
            tmpfullimagepath = os.path.join(request.folder,tmpcompound['imagepath'])
            fullimagepath = os.path.join(request.folder,imagepath)
            os.rename(tmpfullimagepath,fullimagepath)
        except:
            print "ERROR: problem to rename %s"%(tmpcompound['imagepath'])
        
        # get doctmps related to this compoundsubmission
        
        try:
            doctmpdic = db(db.doctmp.compoundsubmission_id==tmpcompoundid).select().as_dict()
            
            # check if doctmp is in doc else is inserted
            for reference, data in doctmpdic.iteritems():
                #check if this reference is stored in doc table
                row = db.doc(doi=data['doi'])
                if not row:
                    docid = db.doc.insert(**db.doc._filter_fields(data))
                else:
                    docid = row.id
                
                db.compound_doc.insert(compound_id=compound_id,
                doc_id=docid
                )
                db(db.doctmp.id==data['id']).update(approved=True)
        except:
            pass
        # insert rdkitstructure
        db.rdkitstructure.insert(
        rdkitstructure=tmpcompound['rdkitstructure'].replace("NID%i"%(tmpcompoundid),"NID%i"%(compound_id)),
        compound_id=compound_id,
        )
        
        # insert mol structure
        db.molstructure.insert(
        molstructure=tmpcompound['molstructure'].replace("NID%i"%(tmpcompoundid),"NID%i"%(compound_id)),
        compound_id=compound_id,
        )
        
        #~ # insert synonyms
        #~ for synonym in tmpcompound['synonym']:
            #~ db.synonym.insert(synonymname=synonym,
            #~ compound_id=compound_id,
            #~ )

        # calculate and insert descriptors
        descriptors = calculate_descriptors(tmpcompound['isosmiles'])
        db.compoundproperty.insert(   
        compound_id = compound_id,
        molecularweight = descriptors["ExactMolWt"],
        tpsa = descriptors["TPSA"],
        numrotatable = descriptors["NumRotatableBonds"],
        logp = descriptors["MolLogP"],
        hbd = descriptors["NumHDonors"],
        hba = descriptors["NumHAcceptors"],
        numring = descriptors["CalcNumRings"],
        #~ molecularvolume = descriptors["MolVol"],
        numro5violation = descriptors["numro5violation"],
        molecularformula = descriptors["molecularformula"], 
        )
        
        
        #~ Field('molecularvolume', type='decimal(10,3)', label="volumen"),
        #~ Field('numn', type='integer'),
        #~ Field('numo', type='integer'),
        #~ Field('nums', type='integer'),

        #~ )    
        
        # Change state of submission to approved
        db(db.compoundsubmission.id==tmpcompoundid).update(approved=True)

        return dict(row={'msj':T('Compound submission ID %i was approved. Now you can access to this compound with the ID %i')%(tmpcompoundid,compound_id)})
    else:
        return dict(row={'msj':T('This submission was closed')})

# COMPOUNDS

def submit_compound_processing(form):
        #check if extension file is .mol
        if IS_UPLOAD_FILENAME(extension='mol')(form.vars.molstructure)[1] == None:
            #check if file is a mol file in correct format
            if is_valid_ctab(form.vars.molstructure.value) == True: 
                pass
            else:
                form.errors.molstructure = T('You must introduce a mol structure file with correct format.')
        elif form.vars.inputsmiles:
            if is_valid_smiles(form.vars.inputsmiles)==True:
                pass
            else: 
                form.errors.inputsmiles = T('SMILES has an error, please check')
        else:
            form.errors.inputsmiles = T('You must introduce an structure using an smiles or uploading a file') 
            
'''
Submition of a new compound. 
This data is store in temporal tables
'''
@auth.requires_login()
def submit_compound():
    
    db.compoundsubmission.source.widget = SQLFORM.widgets.autocomplete(
     request, db.compound.source, limitby=(0,10), min_length=2)
     
    # (1) Build the form
    form = SQLFORM.factory(
        Field('molstructure', type='upload', uploadfolder=os.path.join(request.folder,'static/temp'), comment=T('Structure file only in MOL format')), 
        db.compoundsubmission,
        #~ Field('inputselector',requires=IS_IN_SET(['Smile','Draw','File']),widget=SQLFORM.widgets.radio.widget),
        #~ Field('synonyms', type='list:string', requires=IS_NOT_EMPTY()),
        Field('reference', type='list:string', comment=T('Please insert DOI code of references. Click on + if you have more than one')),
        #~ Field('comment', type='text'),
    )

    # (2) Validate form data
    if form.process(onvalidation=submit_compound_processing).accepted:
        # (3) Insert compound
        compoundsubmission_id = db.compoundsubmission.insert(
            **db.compoundsubmission._filter_fields(form.vars))
        print 'compoundsub %i'%(compoundsubmission_id)
       
        # (3) Insert structure
        # if a mol file was uploaded
        if compoundsubmission_id and form.vars.molstructure:
            molfilename = os.path.join(request.folder,'static/temp/') + form.vars.molstructure
            rdkitmol = Chem.MolFromMolFile(molfilename)
            mol_data = file(molfilename,'r').read()
            cansmiles = Chem.MolToSmiles(rdkitmol)
            isosmiles = Chem.MolToSmiles(rdkitmol,isomericSmiles=True)
            smiles_data = None
            inchi = Chem.MolToInchi(rdkitmol)
            inchikey =Chem.InchiToInchiKey(inchi)
        # if smiles was loaded
        elif compoundsubmission_id and form.vars.inputsmiles:
            rdkitmol = Chem.MolFromSmiles(form.vars.inputsmiles)
            rdkitmol = Chem.AddHs(rdkitmol)
            AllChem.EmbedMolecule(rdkitmol)
            AllChem.UFFOptimizeMolecule(rdkitmol)
            mol_data = Chem.MolToMolBlock(rdkitmol)
            smiles_data = form.vars.inputsmiles
            cansmiles = Chem.CanonSmiles(smiles_data)
            isosmiles = Chem.MolToSmiles(rdkitmol,isomericSmiles=True)
            inchi = Chem.MolToInchi(rdkitmol)
            inchikey =Chem.InchiToInchiKey(inchi)
        
        # (3) Insert reference
        if compoundsubmission_id and form.vars.reference:
            referencelst = form.vars.reference
            # if there is only a reference, this is convert to a list
            if type(referencelst) == str:
                referencelst = [referencelst]
            for reference in referencelst:
                doc = input2doc(reference)
                doc["compoundsubmission_id"]=compoundsubmission_id
                print doc
                db.doctmp.insert(**db.doctmp._filter_fields(doc))
            #~ elif not row.nearest: 
                #~ row.update_record(nearset=nearest)
        else: pass # do nothing 
        
        #create molecular image from smiles 
        if compoundsubmission_id:   
            imagepath = settings.imagedir+"nid_tmp" + str(compoundsubmission_id)+".png"
            row = db(db.compoundsubmission.id==compoundsubmission_id).select().first()
            row.update_record(imagepath=imagepath)
            fullimagepath = os.path.join(request.folder,imagepath)
            create_molimage(isosmiles,fullimagepath)
            
            #replace line 1 and 2 of mol structure
            mol_datadiv = mol_data.split("\n")
            mol_datadiv[0] = "NID%i"%(compoundsubmission_id)
            mol_datadiv[1]= "NaturAr Database"
            mol_data="\n".join(mol_datadiv)    
            # Add smiles and structures
            db.executesql("UPDATE compoundsubmission SET inputsmiles ='%s'::cstring, molstructure ='%s'::cstring, rdkitstructure =mol_from_ctab('%s'::cstring), addinfo='%s'::cstring, isosmiles='%s'::cstring, cansmiles='%s'::cstring, inchi='%s'::cstring, inchikey='%s'::cstring WHERE id='%i';"%(smiles_data, mol_data, mol_data, form.vars.addinfo, isosmiles, cansmiles, inchi, inchikey, compoundsubmission_id))
            response.flash = T('Compound has been uploaded successfully.')
        else:
            response.flash = T('Your submission had a problem. Please contact the administrator. Thanks')
    content = form
  
    return dict(content=content)


@auth.requires_login()
def compound_submitted():
    """
    action to show a list of compounds
    """
    db.compoundsubmission.created_on.readable = True
    imagewidth = 70
    imageheight = 70
    #~ db.compoundsubmission.synonym = Field.Virtual('synonym', synonymlist)
    #~ db.compoundsubmission.id.readable = False
    query = db(db.compoundsubmission.approved==False and db.compoundsubmission.created_by==auth.user_id)
    form = SQLFORM.grid(query,create=False,editable=True,deletable=True,     
    links=[dict(header=T('Image'), body = lambda row: DIV(IMG(_src=URL('.',row.imagepath), _width=imagewidth, _height=imageheight),_class="img-zoom"))],        
    paginate=10,
        fields=[db.compoundsubmission.id ,db.compoundsubmission.created_on, db.compoundsubmission.inputsmiles,db.compoundsubmission.source,db.compoundsubmission.synonym,db.compoundsubmission.imagepath ])
    
    
    if request.args(0):
        if "view" in request.args(0) or "edit" in request.args(0):
            compound_id = request.args(2)
             # Docs selection
            docs_id = db(db.doctmp.compoundsubmission_id==compound_id).select(db.doctmp.id).as_list()
            print docs_id
            if docs_id!=[]:
                doclst = []
                for doc in docs_id:
                    table = db(db.doctmp.id==doc['id']).select(
                        db.doctmp.journal,
                        db.doctmp.year,
                        db.doctmp.volume,
                        db.doctmp.issue,
                        db.doctmp.firstpage,
                        db.doctmp.lastpage,
                        db.doctmp.doi,
                        db.doctmp.isbn10,
                        db.doctmp.issn,
                        db.doctmp.pubmed_id,
                        db.doctmp.title,
                        db.doctmp.doctype,
                        db.doctmp.authors,
                        db.doctmp.abstract,
                        db.doctmp.url,
                        )
                    doclst.append(table.first())                    
            else:
                doclst = None
            
            # Molfile generation
            
            

    else:
        doclst = None
        compound_id = ""
    
    properties = ""

    #~ print doi2doc("10.1016/j.molstruc.2014.10.054")['message']['author']
   
    return dict(form=form, docs=doclst, properties=properties, compound_id=compound_id)       
        

