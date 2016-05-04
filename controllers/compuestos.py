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
    #~ rows=db().select(db.compound.ALL,limitby=limitby)
    #~ return dict(rows=rows,page=page,items_per_page=items_per_page)


def list_molecules2():
    grid = SQLFORM.smartgrid(db.compound, paginate=5)
    return locals()

#~ @auth.requires_membership('managers')
def buscar():
    """
    action to show a list of compounds
    """
    imagewidth = 70
    imageheight = 70
    request.is_local =False
    #extract of http://stackoverflow.com/questions/21447804/web2py-sqlform-grid-edit-page
    db.compound.id.readable = False
    db.compound.id.writeable = False
 

    form = SQLFORM.grid(
        query=db.compound,
        formname="compound",
        editable = auth.has_membership('managers'),
        deletable = auth.has_membership('managers'),
        buttons_placement = 'left',
        paginate = 5,
        searchable= dict(smiles=True, extract=False),
        links=[dict(header=T('Image'), body = lambda row: 
        DIV(A(IMG(_src=URL('static',row.imagepath), 
        _width=imagewidth, _height=imageheight),_href="localhost"),_class="img-zoom"))])
        
   
   
    #if "view" in request.args(0)request.env.request_uri:
    #~ try:
    if request.args(0):
        if "view" in request.args(0):
            record_id = form.view_form.record_id 
            # Properties selection
            table = db(db.compound_property.compound_id==record_id).select(
                db.compoundproperty.molecular_weight,
                db.compoundproperty.molecular_formula,
                db.compoundproperty.molecular_volume,
                db.compoundproperty.smiles,
                db.compoundproperty.clogp,
                db.compoundproperty.xlogp,
                db.compoundproperty.tpsa,
                db.compoundproperty.hbd,
                db.compoundproperty.hba,
                db.compoundproperty.num_rotatables_bonds,
                db.compoundproperty.aromatic_rings,
                db.compoundproperty.num_n,
                db.compoundproperty.num_o,
                db.compoundproperty.num_s,
                db.compoundproperty.num_ro5_violations,
            )        
            properties = rows_transpose(table)
            
            # Docs selection
            docs_id = db(db.compound.id==record_id).select(db.compound.docs)
            try:
                table = db(db.doc.id.belongs(docs_id.first().docs)).select(
                    db.doc.journal,
                    db.doc.year,
                    db.doc.volume,
                    db.doc.issue,
                    db.doc.first_page,
                    db.doc.last_page,
                    db.doc.doi,
                    db.doc.pubmed_id,
                    db.doc.title,
                    db.doc.doc_type,
                    db.doc.authors,
                    db.doc.abstract,
                )            
                docs = rows_transpose(table)
            except:
                docs=None

    else:
        properties = ""
        docs = ""
    
    
    print doi2doc("10.1016/j.molstruc.2014.10.054")['message']['author']
   
    return dict(form=form, properties=properties, docs=docs)
    
def buscar2():
    """
    action to show a list of compounds
    """
    imagewidth = 70
    imageheight = 70
    request.is_local =False
    #extract of http://stackoverflow.com/questions/21447804/web2py-sqlform-grid-edit-page
    db.compound.id.readable = False
    db.compound.id.writeable = False
 

    form = SQLFORM.smartgrid(db.compound,
        #~ left=db.extract_record.extract_name(db.extract_record.id==db.compound.extract),
        editable = auth.has_membership('managers'),
        deletable = auth.has_membership('managers'),
        buttons_placement = 'left',
        paginate = 5,
        searchable= dict(smiles=True, extract=False),
        #~ links=[dict(header=T('Image'), body = lambda row: 
        #~ DIV(A(IMG(_src=URL('static',row.imagepath), 
        #~ _width=imagewidth, _height=imageheight),_href="localhost"),_class="img-zoom"))]
        )
               

    print calculate_descriptors("NN")
   
    return dict(form=form)    
    

def custom_search():
    '''
    Implements SQLFORM.grid custom search 
        WITHOUT specifying a custom search_widget,
            and so needing to read & understand the clever web2py implementation source code.
    The custom_search.html view contains the EASIER TO UNDERSTAND customization code.
    The technique:
        1. Make the grid's Standard Search Input hidden.
        2. Define Custom Search Input elements 
            with onchange events that 
                send their values to the to the hidden Standard Search Input.
    '''
    query=((db.compound.id > 0))
    fields = (db.compound.id, 
        db.compound.smiles, 
        db.compound.name, 
        )
 
    headers = {'compound.id':   'ID',
           'compound.smiles': 'Last Name',
           'db.compound.name': 'Primary Phone',
           }    
    init_sort_order=[db.compound.name]   
 
    grid = SQLFORM.grid(query=query, 
        fields=fields, 
        headers=headers, 
        orderby=init_sort_order,
        searchable=True,  
        user_signature=False, 
        create=True, deletable=False, editable=True, maxtextlength=100, paginate=25)
 
    return dict(grid=grid)  




def manage_packages():
    if request.args(0) == 'new' and request.args(1) == 'compound':

        # (1) Get available docs
        docs = [(r.id, r.title) for r in db(db.doc).select()]
        print docs

        # (2) Build the form
        form = SQLFORM.factory(
            db.compound,
            Field('doc',
                requires=IS_IN_SET(docs, multiple=True)
            )
        )

        # (3) Validate form data
        if form.process().accepted:

            # (4) Insert compound
            compound_id = db.compound.insert(
                **db.compound._filter_fields(form.vars))

            if compound_id and form.vars.docs:

                # (5) Insert component package associations
                for doc_id in form.vars.docs:
                    existing_doc = db.doc(doc_id)

                    if existing_doc:
                        db.r_compound_doc.insert(
                            compound_id=compound_id,
                            doc_id=existing_doc
                        )

                response.flash = 'Package has been created successfully.'

        content = form
    else:
        content = SQLFORM.grid(db.compound)

    return dict(content=content)



def two_forms():
    
    form1 = FORM(INPUT(_name='form_one', requires=IS_NOT_EMPTY()),
               INPUT(_type='submit'))
    form2 = FORM(INPUT(_name='form_two', requires=IS_NOT_EMPTY()),
               INPUT(_type='submit'))
    form3 = SQLFORM.grid(query=db.compound,
        formname="compound_doc")

    if form1.process(formname='form_one').accepted:
        response.flash = 'form one accepted'
    if form2.process(formname='form_two').accepted:
        response.flash = 'form two accepted'
    return dict(form1=form1, form2=form2, form3=form3)
    
    
def upload():
     # (1) Get available components
    compounds = [(r.id, r.compoundname) for r in db(db.compound).select()]

    # (2) Build the form
    form = SQLFORM.factory(
        db.classification,
        Field(
            'compounds',
            requires=IS_IN_SET(compounds, multiple=True)
        )
    )
    print compounds

    # (3) Validate form data
    if form.process().accepted:

        # (4) Insert package
        classification_id = db.classification.insert(
            **db.classification._filter_fields(form.vars))

        if classification_id and form.vars.compounds:

            # (5) Insert component package associations
            for compound_id in form.vars.compounds:
                existing_compound = db.compound(compound_id)

                if existing_compound:
                    db.compound_classification.insert(
                        classification_id=classification_id,
                        compound_id=existing_compound
                    )

            response.flash = 'Package has been created successfully.'

    content = form
    #~ else:
        #~ content = SQLFORM.grid(db.classification)

    return dict(content=content)
    
def upload2():
     # (1) Get available classifications
    classifications = [(r.id, r.classificationname) for r in db(db.classification).select()]
    chemicalclasses = [(r.id, r.classname_en) for r in db(db.chemicalclass).select()]
    #~ extracts = [(r.id, r.extractname) for r in db(db.chemicalclass).select()]

    # (2) Build the form
    form = SQLFORM.factory(
        db.compound,
        Field('classifications',
            requires=IS_IN_SET(classifications, multiple=True)),
        Field('chemicalclasses',
            requires=IS_IN_SET(chemicalclasses, multiple=True)),
        Field('synonyms', type='text', requires=IS_NOT_EMPTY()),
    )
    # (3) Validate form data
    if form.process().accepted:

        # (4) Insert compound
        compound_id = db.compound.insert(
            **db.compound._filter_fields(form.vars))
        
        # (5) Insert compound_classification associations
        if compound_id and form.vars.classifications:
            for classification_id in form.vars.classifications:
                existing_classification = db.classification(classification_id)
                if existing_classification:
                    db.compound_classification.insert(
                        compound_id=compound_id,
                        classification_id=existing_classification)
                        
        # (6) Insert compound_chemicalclass associations
            
        if compound_id and form.vars.chemicalclasses:
            for chemicalclass_id in form.vars.chemicalclasses:
                existing_chemicalclass = db.chemicalclass(chemicalclass_id)
                if existing_chemicalclass:
                    db.compound_chemicalclass.insert(
                        compound_id=compound_id,
                        chemicalclass_id=existing_chemicalclass)
                        
        # (7) Insert synonyms
        if compound_id and form.vars.synonyms:
            synonymlist = form.vars.synonyms.split('\n')
            for synonym in synonymlist:
                db.synonym.insert(
                    compound_id=compound_id,
                    synonymname=str(synonym).strip('\r'))
                        

        response.flash = T('Compound has been uploaded successfully.')

    content = form
    #~ else:
        #~ content = SQLFORM.grid(db.compound)

    return dict(content=content)




def upload_molprocessing(form):
        #check if extension file is .mol
        if IS_UPLOAD_FILENAME(extension='mol')(form.vars.molstructure)[1] == None:
            #check if file is a mol file in correct format
            if is_valid_ctab(form.vars.molstructure.value) == True: 
                pass
            #~ inputmolrdkit = Chem.MolFromMolFile(form.vars.molstructure.file)
            #~ inputmolfile = os.path.join(request.folder,'static/temp/') + form.vars.molstructure
            else:
                form.errors.molstructure = T('You must introduce a mol structure file with correct format.')
        elif form.vars.isosmiles:
            if is_valid_smiles(form.vars.isosmiles)==True:
                pass
            else: 
                form.errors.isosmiles = T('SMILES has an error, please check')
        else:
            form.errors.isosmiles = T('You must introduce an structure using an smiles or uploading a file')  

def upload3():
     # (1) Get available classifications
    classifications = [(r.id, r.classificationname) for r in db(db.classification).select()]
    chemicalclasses = [(r.id, r.classname_en) for r in db(db.chemicalclass).select()]
    #~ extracts = [(r.id, r.extractname) for r in db(db.chemicalclass).select()]

    # (2) Build the form
    form = SQLFORM.factory(
        Field('molstructure', type='upload', uploadfolder=os.path.join(request.folder,'static/temp')), 
        #~ requires = IS_UPLOAD_FILENAME(extension='mol')),
        db.compound,
        Field('classifications',
            requires=IS_IN_SET(classifications, multiple=True)),
        Field('chemicalclasses',
            requires=IS_IN_SET(chemicalclasses, multiple=True)),
        #~ Field('inputselector',requires=IS_IN_SET(['Smile','Draw','File']),widget=SQLFORM.widgets.radio.widget),
        Field('synonyms', type='list:string', requires=IS_NOT_EMPTY()),
    )
    
    # (3) Validate form data
    if form.process(onvalidation=upload_molprocessing).accepted:

        # (4) Insert compound
        compound_id = db.compound.insert(
            **db.compound._filter_fields(form.vars))
        
        # (5) Insert compound_classification associations
        if compound_id and form.vars.classifications:
            for classification_id in form.vars.classifications:
                existing_classification = db.classification(classification_id)
                if existing_classification:
                    db.compound_classification.insert(
                        compound_id=compound_id,
                        classification_id=existing_classification)
                        
        # (6) Insert compound_chemicalclass associations
        if compound_id and form.vars.chemicalclasses:
            for chemicalclass_id in form.vars.chemicalclasses:
                existing_chemicalclass = db.chemicalclass(chemicalclass_id)
                if existing_chemicalclass:
                    db.compound_chemicalclass.insert(
                        compound_id=compound_id,
                        chemicalclass_id=existing_chemicalclass)
                        
        # (7) Insert synonyms
        if compound_id and form.vars.synonyms:
            synonymlist = form.vars.synonyms
            for synonym in synonymlist:
                db.synonym.insert(
                    compound_id=compound_id,
                    synonymname=str(synonym).strip('\r'))
        
        # (8) Insert structure
        if compound_id and form.vars.molstructure:
            filename = os.path.join(request.folder,'static/temp/') + form.vars.molstructure
            mol_data = file(filename,'r').read()
            db.executesql("insert into structure (molstructure,compound_id) VALUES (mol_from_ctab('%s'::cstring), '%i');"%(mol_data,compound_id))
        elif compound_id and form.vars.isosmiles:
            db.executesql("insert into structure (molstructure,compound_id) VALUES (mol_from_smiles('%s'::cstring), '%i');"%(form.vars.isosmiles,compound_id))
            
        
        #~ inputmolfile = os.path.join(request.folder,'static/temp/') + form.vars.molstructure
        #~ inputmolrdkit = Chem.MolFromMolFile(inputmolfile)
        #~ if inputmolrdkit == None:
        #~ print inputmolrdkit
        response.flash = T('Compound has been uploaded successfully.')


    content = form
    #~ else:
        #~ content = SQLFORM.grid(db.compound)

    return dict(content=content)