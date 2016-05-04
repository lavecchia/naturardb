# RdKit nexo con paquete
#
from rdkit import Chem
from rdkit.Chem import Descriptors
         
       
#ejemplos RDKIT con postgresql
#~ a = db.executesql('select * into prueba from (select id,mol_from_smiles('ccc'::cstring) m from compound_record) tmp where m is not null;')
#a = db.executesql(("INSERT INTO com (id,m) VALUES (29,mol_from_smiles('%s'::cstring));")%("CCC"))
#~ a = db.executesql('select * from prueba where m@>%s',('CCC',))
#~ a = db.executesql('select morgan_fp(m) from prueba where m@>%s',('CCC',))
#~ a = db.executesql("select is_valid_smiles('CC'::cstring);")


#~ a = db.executesql("select * from compound_structure where molstructure@>'C' limit 100;")


# POPURRI
# - instalacion RDKit database cartridge http://www.rdkit.org/docs/Cartridge.html
# - edicion consola psql naturardb -U fito
# - postgre 123456
# - psql -c 'create extension rdkit' naturardb


# COMMON FUNCTIONS

def create_molimage(smiles,imagepath):
    """
    check if the image was created if not it is generated, and return the path
    """
    mol = Chem.AllChem.MolFromSmiles(smiles)
    imagepath = "applications/naturar/static/"+imagepath
    Chem.Draw.MolToFile(mol,imagepath,size=(200,200))


def is_valid_smiles(smiles):
    '''
    check if a smiles is valid
    '''
    return db.executesql("select is_valid_smiles('%s'::cstring);"%(smiles))[0][0]
    
    
def is_valid_ctab(molblock):
	'''
	check if a mol block is valid
	'''
	return db.executesql("select is_valid_ctab('%s'::cstring);"%(molblock))[0][0]


#~ 
#~ def mol_from_ctab(molblock):
	#~ '''
	#~ insert a mol block
	#~ '''
	#~ return db.executesql("select mol_from_ctab('%s'::cstring);"%(molblock))[0][0]
#~ 
#~ 
#~ 

def calculate_descriptors(smiles):
    '''
    calculate a list of descriptors and return a dictionary with calculated values
    '''
    molecule = Chem.MolFromSmiles(smiles)
    
    descriptorlst = [
    "ExactMolWt", 
    "TPSA",
    "NumRotatableBonds",
    "MolLogP",
    "NumHDonors",
    "NumHAcceptors",
    ]
    
    descriptorvaluedic = {}
    for descriptor in descriptorlst:
        descriptorvaluedic[descriptor] = getattr(Chem.Descriptors, descriptor)(molecule)
    
    return descriptorvaluedic
    

