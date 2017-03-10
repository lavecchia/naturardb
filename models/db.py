# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig

## to use mol field of RDKIT
from gluon.dal import SQLCustomType

## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)



#~ if not request.env.web2py_runtime_gae:
    #~ ## if NOT running on Google App Engine use SQLite or other DB
    #~ db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
#~ else:
    #~ ## connect to Google BigTable (optional 'google:datastore://namespace')
    #~ db = DAL('google:datastore+ndb')
    #~ ## store sessions and tickets there
    #~ session.connect(request, response, db=db)
    #~ ## or store session in Memcache, Redis, etc.
    #~ ## from gluon.contrib.memdb import MEMDB
    #~ ## from google.appengine.api.memcache import Client
    #~ ## session.connect(request, response, db = MEMDB(Client()))
    #~ 
db = DAL("postgres://fito:123456@localhost:5432/naturardb")
#~ db = DAL("postgres://fito:123456@localhost/naturardb", migrate=True, fake_migrate=True,)
#~ db = DAL("postgres://fito:123456@localhost/naturardb", migrate=False, fake_migrate=True,)

#~ db = DAL("postgres://fito:123456@localhost/naturardb", migrate=True)

#~ db = DAL("postgres://fito:123456@localhost/naturardb", lazy_tables=True)

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## extra fields (mjl)
auth.settings.extra_fields['auth_user']= [
    Field('address', type='string', label=T('Address')),
    Field('phone', type='string', label=T('Phone')),
    Field('picture', type='upload', label=T('Picture')),
    Field('rearchdescription', type='text', label=T('Research Description')),
    Field('additionalinfo', type='text', label=T('Additional Information')),
    ]


## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False) 


## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True


#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

# --------------------------------------------------------------------
# SETTINGS
# --------------------------------------------------------------------


#~ settings.max_size # get the value
#~ settings.update_record(summary=new_summary) # set a value 
db.define_table('settings', 
    Field('imagedir', default="applications/naturar/images_molecule/"),
    #~ Field('max_size', 'integer', default=10),
    #~ Field('summary', 'text', 'abc'),
)
# create an instance of settings table
settings = db(db.settings.id > 0).select().first()
if not settings:
    settings = db.settings.insert()

# --------------------------------------------------------------------    
# LOCATION
# --------------------------------------------------------------------

'''data is extrated of Yahoo and Google webservices '''
db.define_table('location',  
    auth.signature,
    Field('country', type='string'),
    Field('state', type='string'),
    Field('city', type='string'),
    Field('place', type='string'),
    Field('latitude', type='double'),
    Field('longitude', type='double'),
    Field('yahoowoeid', type='integer'),
    Field('googleplaceid', type='string'),
    Field('placetypename', type='string'),
    )


# --------------------------------------------------------------------
# DOCS
# --------------------------------------------------------------------

'''
Store bibliographic information, this can be obtained from Crossref API
'''
db.define_table('doc', 
    auth.signature,
    Field('journal', type='string'),
    Field('year', type='datetime', requires = IS_DATE(format=('%Y'))),
    Field('volume', type='integer'),
    Field('issue', type='integer'),
    Field('firstpage', type='integer'),
    Field('lastpage', type='integer'),
    Field('doi', type='string'),
    Field('isbn', type='string'),
    Field('pubmed_id'),
    Field('title', type='text'),
    Field('doctype', type='string'),
    Field('authors'),
    Field('abstract', type='text'),
    Field('url', type='text'),
    )


# --------------------------------------------------------------------
# COMPOUND INFORMATION
# --------------------------------------------------------------------

'''
Store compound information
'''
db.define_table('compound', 
    auth.signature,
    #~ Field('compoundname', requires=IS_NOT_EMPTY()),
    #~ Field('iupacname', type='string'),
    Field('inchi', type='string', readable=False, writable=False),
    Field('inchikey', type='string', readable=False, writable=False),
    Field('isosmiles', type='string'),
    Field('cansmiles', type='string', readable=False, writable=False),
    Field('imagepath', type='text', readable=False, writable=False),
    Field('addinfo', type='text'), 
    Field('approved', type='boolean', readable=False, writable=False), 
    #~ format='c%(id)i-%(name)s',
    )
    
'''
Many to many table relationship: Docs and Compounds
'''
db.define_table('compound_doc',
    auth.signature,
    Field('compound_id', 'reference compound'),
    Field('doc_id', 'reference doc'),
    )

'''
Structures (rdkit mol type) of compounds
'''
#~ db.executesql('CREATE TABLE IF NOT EXISTS structure ( \
    #~ id integer NOT null, \
    #~ molstructure MOL, \
    #~ compound_id int references compound(id), \
    #~ CONSTRAINT structure_pk PRIMARY KEY (id));')
mol = SQLCustomType(
    type ='text',
    native ='mol',
    )

db.define_table('rdkitstructure',
    auth.signature,
    Field('rdkitstructure', type=mol),
    Field('compound_id', 'reference compound'),
    )

'''
Structures (mol file type) of compounds
'''
db.define_table('molstructure',
    auth.signature,
    Field('molstructure', type='text'),
    Field('compound_id', 'reference compound'),
    )

'''
Store descriptors of 3D structures
'''
db.define_table('structuredescriptor',
    auth.signature,
    Field('methodname', type='string')
    )
    
'''
Many to many table relationship: StructureDescriptors and Rdkitstructures
'''
db.define_table('structure_descriptor',
    auth.signature,
    Field('structuredescriptor_id', 'reference structuredescriptor'),
    Field('structure_id', 'reference rdkitstructure'),
    Field('descriptorvalue', type='decimal(10,4)'),
    )    

'''
Types of compound synomys
'''
db.define_table('synonymtype',
    auth.signature,
    Field('synonymtype', type='string'),
    ) 

'''
Store synonyms of compound names
'''
db.define_table('synonym',
    auth.signature,
    Field('synonymtype_id', 'reference synonymtype'),
    Field('synonymname', type='string'),
    Field('compound_id', 'reference compound'),
    )    

'''
List of compound classification, active.
'''
db.define_table('classification',
    auth.signature,
    Field('classificationname', type='string'),
    Field('classificationdescription', type='text'),
    )

'''
Many to many table relationship: Classification and Compounds
'''
db.define_table('compound_classification',
    auth.signature,
    Field('compound_id', 'reference compound'),
    Field('classification_id', 'reference classification'),
    )
    
'''
List of compound class,  
fuctional groups, ej aminas, sulfonamidas, etc.
'''
db.define_table('chemicalclass',
    auth.signature,
    Field('classname_en', type='string'),
    Field('classname_es', type='string'),
    Field('classdescription', type='text'),
    )

'''
Many to many table relationship: Chemicalclass and Compounds,
'''
db.define_table('compound_chemicalclass',
    auth.signature,
    Field('compound_id', 'reference compound'),
    Field('chemicalclass_id', 'reference chemicalclass'),
    )
    
'''
Define isomer relationships between two compounds
'''
db.define_table('isomer',
    auth.signature,
    Field('compound1_id', 'reference compound'),
    Field('compound2_id', 'reference compound'),
    )


#~ # define autocomplete function for extracto
#~ db.compound_record.extract.widget = SQLFORM.widgets.autocomplete(
     #~ request, db.extract_record.extract_name, id_field=db.extract_record.id, limitby=(0,10), min_length=2)

'''
List of calculated properties
'''
db.define_table('compoundproperty', 
    auth.signature,
    Field('compound_id', 'reference compound'),
    Field('molecularweight', type='decimal(10,4)'),
    Field('molecularformula', type='string'),
    Field('molecularvolume', type='decimal(10,3)', label="volumen"),
    Field('logp', type='decimal(10,4)'),
    Field('tpsa', type='decimal(10,4)'),
    Field('hbd', type='integer'),
    Field('hba', type='integer'),
    Field('numrotatable', type='integer'),
    Field('numring', type='integer'),
    Field('numn', type='integer'),
    Field('numo', type='integer'),
    Field('nums', type='integer'),
    Field('numro5violation', type='integer'),
    )

'''
List of extra properties
'''
db.define_table('extraproperty', 
    auth.signature,
    Field('extrapropertyname_en', type='string'),
    Field('extrapropertyname_es', type='string'),
    )

'''
Many to many table relationship: Extraproperty and Compounds,
'''
db.define_table('compound_extraproperty',
    auth.signature,
    Field('compound_id', 'reference compound'),
    Field('extraproperty_id', 'reference extraproperty'),
    Field('extrapropertyvalue')
    )


# --------------------------------------------------------------------
# SOURCE INFORMATION
# --------------------------------------------------------------------

''' 
Table where is stored source information obtained frod databases like 
Catalogue of Life using webservices.
dbname is the name of the database whereis is obtained the data and 
idfromdb is the original ID code.
'''
db.define_table('source', 
    auth.signature,
    Field('scientificname', type='string'),
    Field('sourcekingdom', type='string'),
    Field('sourcefamily', type='string'),
    Field('sourcegenus', type='string'),
    Field('sourcespecies', type='string'),
    Field('variety', type='string'),
    Field('ethnomedicinalinfo', type='text'),
    Field('dbname', type='string'),
    Field('idfromdb', type='string'),
    )

'''
Images of sources
'''
db.define_table('sourceimage',
    auth.signature,
    Field('source_id', 'reference source'),
    Field('sourceimage', type='string'),
    Field('credit', type='string'),
    )

'''
Native names of a source
'''
db.define_table('nativename',
    auth.signature,
    Field('source_id', 'reference source'),
    Field('nativename', type='string'),
    Field('culture', type='string'),
    )
    
'''
Common names of a source
'''
db.define_table('commonname',
    auth.signature,
    Field('source_id', 'reference source'),
    Field('commonname', type='string'),
    )
    
'''
Medicinal Uses
'''
db.define_table('medicinal',
    auth.signature,
    Field('medicinaluse_en', type='string'),
    Field('medicinaluse_es', type='string'),
    )

'''
Many to many table relationship: Medicinal Uses and Sources
'''
db.define_table('source_medicinal',
    auth.signature,
    Field('source_id', 'reference source'),
    Field('medicinal_id', 'reference medicinal'),
    )
    
'''
Food Uses
'''
db.define_table('food',
    auth.signature,
    Field('fooduse_en', type='string'),
    Field('fooduse_es', type='string'),
    )

'''
Many to many table relationship: Food Uses and Sources
'''
db.define_table('source_food',
    auth.signature,
    Field('source_id', 'reference source'),
    Field('food_id', 'reference food'),
    )


'''
Other Uses
'''
db.define_table('otheruse',
    auth.signature,
    Field('otherusename', type='string'),
    )

'''
Many to many table relationship: Other Uses and Sources
'''
db.define_table('source_otheruse',
    auth.signature,
    Field('source_id', 'reference source'),
    Field('otheruse_id', 'reference otheruse'),
    )

'''
Many to many table relationship: Location and Sources
'''
db.define_table('source_location',
    auth.signature,
    Field('source_id', 'reference source'),
    Field('location_id', 'reference location'),
    )

'''
Many to many table relationship: Docs and Sources
'''
db.define_table('source_doc',
    auth.signature,
    Field('source_id', 'reference source'),
    Field('doc_id', 'reference doc'),
    )
     
     
# --------------------------------------------------------------------
# USERS (cont.)
# --------------------------------------------------------------------

'''
Store internal messages between members
'''
db.define_table('message',
    auth.signature,
    Field('messagetitle', type='string'),
    Field('messagebody', type='text'),
    Field('usersent_id', 'reference auth_user'),
    Field('userreceiver_id', 'reference auth_user'),
    Field('date', type='datetime'),
    )

'''
Research groups
'''
db.define_table('researchgroup',
    auth.signature,
    Field('reseachname', type='string'),
    Field('institution', type='string'),
    Field('webpage', type='string'),
    Field('email', type='string'),
    Field('telephone', type='string'),
    Field('address', type='string'),
    Field('location_id', 'reference location'),
    Field('logo', type='upload'),
    )
    
'''
Many to many table relationship: Research Groups and Users
'''
db.define_table('user_reseach',
    auth.signature,
    Field('user_id', 'reference auth_user'),
    Field('researchgroup_id', 'reference researchgroup'),
    )
    
'''
Many to many table relationship: Docs and Users
'''
db.define_table('user_doc',
    auth.signature,
    Field('user_id', 'reference auth_user'),
    Field('doc_id', 'reference doc'),
    )   

'''
Many to many table relationship: Compounds and Users to store in profile 
'''
db.define_table('bookmark',
    auth.signature,
    Field('user_id', 'reference auth_user'),
    Field('compound_id', 'reference compound'),
    )   


# --------------------------------------------------------------------
# EXTRACTS
# --------------------------------------------------------------------

'''
List of part from where you can obtain extract
'''
db.define_table('partused',
    auth.signature,
    Field('partname_en'),
    Field('partname_es'),
    )

'''
Main table of extract
'''
db.define_table('extract', 
    auth.signature,
    Field('source_id', 'reference source'),
    Field('location_id', 'reference location'),
    Field('partused_id', 'reference partused'),
    Field('extractpreparation', type='text'),
    format='%(extract_name)s',
    )

'''
Many to many table relationship: Docs and Extract
'''
db.define_table('extract_doc',
    auth.signature,
    Field('extract_id', 'reference extract'),
    Field('doc_id', 'reference doc'),
    )

'''
Many to many table relationship: Compound and Extract
'''
db.define_table('compound_extract',
    auth.signature,
    Field('extract_id', 'reference extract'),
    Field('compound_id', 'reference compound'),
    Field('compoundamount', type='double'),
    )


# --------------------------------------------------------------------
# ASSAYS
# --------------------------------------------------------------------

'''
List of assays
'''
db.define_table('assay',
    auth.signature,
    Field('assayname', type='string'),
    Field('assaydescription', type='text'),
    Field('pubchecbioassay_id'),
    )

'''
Many to many table relationship: Assay and Extract
'''
db.define_table('extract_assay',
    auth.signature,
    Field('extract_id', 'reference extract'),
    Field('compound_id', 'reference compound'),
    Field('compoundamount', type='double'),    
    Field('inhibition', type='double'),
    Field('activity', type='double'),
    Field('cytotoxicity', type='double'),
    Field('sideEffects', type='text'),
    )

'''
Many to many table relationship: Docs and Assay
'''
db.define_table('assay_doc',
    auth.signature,
    Field('assay_id', 'reference assay'),
    Field('doc_id', 'reference doc'),
    )

'''
List of assay targets
'''
db.define_table('target',
    auth.signature,
    Field('targetname', type='string'),
    )

'''
Many to many table relationship: Target and Assay
'''
db.define_table('assay_target',
    auth.signature,
    Field('assay_id', 'reference assay'),
    Field('target_id', 'reference target'),
    )


# --------------------------------------------------------------------
# COMPOUND SUBMISSION
# --------------------------------------------------------------------
'''
Compound submission, create a temporal compound and then, if all are right, it is approved.
'''
db.define_table('compoundsubmission',
	auth.signature,
	Field('inputsmiles', type='string'),
	Field('inchi', type='string', readable=False, writable=False),
    Field('inchikey', type='string', readable=False, writable=False),
    Field('isosmiles', type='string', readable=False, writable=False),
    Field('cansmiles', type='string', readable=False, writable=False),
    Field('molstructure', type='text', readable=False, writable=False),
    Field('rdkitstructure', type=mol, readable=False, writable=False),
	Field('state', type='string', readable=False, writable=False),
    Field('addinfo', type='text', readable=False, writable=False),
    )

'''
Store temporal synonym names of submited compounds
'''
db.define_table('tmpsynonym',
    auth.signature,
    Field('synonymname', type='string'),
    Field('compoundsubmission_id', 'reference compoundsubmission'),
    )  

'''
Store temporal bibliographic information, this can be obtained from Crossref API
'''
db.define_table('tmpdoc', 
    auth.signature,
    Field('journal', type='string'),
    Field('year', type='datetime', requires = IS_DATE(format=('%Y'))),
    Field('volume', type='integer'),
    Field('issue', type='integer'),
    Field('firstpage', type='integer'),
    Field('lastpage', type='integer'),
    Field('doi', type='string'),
    Field('isbn10', type='string'),
    Field('issn', type='string'),
    Field('pubmed_id'),
    Field('title', type='text'),
    Field('doctype', type='string'),
    Field('authors'),
    Field('abstract', type='text'),
    Field('url', type='text'),
    )
    
'''
Many to many table relationship: Tmpdocs and Tmpcompounds
'''
db.define_table('tmpcompound_tmpdoc',
    auth.signature,
    Field('compoundsubmission_id', 'reference compoundsubmission'),
    Field('doc_id', 'reference tmpdoc'),
    )

## after defining tables, uncomment below to enable auditing
#~ auth.enable_record_versioning(db)
