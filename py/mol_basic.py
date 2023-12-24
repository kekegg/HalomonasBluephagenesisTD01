# from IPython.display import SVG
import numpy as np

from rdkit import Chem
from rdkit.Chem import rdDepictor as rdd
from rdkit.Chem.Draw import rdMolDraw2D as draw2d
from rdkit.Chem import Descriptors
import math

def get_closest(p, atoms, r):
    ii = -1
    dis = 10000000
    x = float(p[0])
    y = float(p[1])
    for (i, item) in enumerate(atoms):
        r = math.sqrt((x - item[0])**2 + (y-item[1])**2)
#         print(r)
        if r < dis:
            dis = r
            ii = i
    return ii

def modify_svg(svg):
    svgarr = svg.split('\n')
    new_arr = []
    pathMask_arr = []
    ellipse_arr = []
    atoms_coor = []
    # other_arr = []
    cnt = 0
    r = 0
    bond_mask_flag = 1
    bond_mask_cnt = 0
    start_append = 0
    for ln in svgarr:
        # arr = re.split(' ', ln)
        arr = ln.split(" ")
#         if arr[0] == "<path" and bond_mask_flag:
#             arr2 = [arr[0]] + ['id="bondMask_' + str(bond_mask_cnt) +'"'] + ['class="bondArea"'] + ['onclick=\'addBondClick(event,"'+ str(bond_mask_cnt) + '")\''] + arr[1:]
#             bond_mask_cnt = bond_mask_cnt + 1
#             n_ln = " ".join(arr2)
#             pathMask_arr.append(n_ln)
        # else:
        #     if start_append and arr[0] != "</svg>":
        #         new_arr.append(ln)

        if arr[0] == "<rect":
            start_append = 1

        if arr[0] == "<ellipse":
            bond_mask_flag = 0
            arr2 = [arr[0]] + ['id="atom_' + str(cnt) +'"'] + ['class="atomArea"'] + ['onclick=\'addFragClick(event,"'+ str(cnt) + '")\''] + ['oncontextmenu=\'rightClick(event,"'+ str(cnt) + '")\''] + arr[1:]
            n_ln = " ".join(arr2)
            # print(n_ln)
            tp_arr = arr[1].split('\'')
            tp_arr2 = arr[2].split('\'')
            tp_arr3 = arr[3].split('\'')
            r = r + float(tp_arr3[1])
            atoms_coor.append([float(tp_arr[1]), float(tp_arr2[1])])
            cnt = cnt + 1
            ellipse_arr.append(n_ln)
        
        if arr[0] == "<path" and not bond_mask_flag:
            new_arr.append(ln)
        
        if arr[0] == "<text":
            new_arr.append(ln)
    
    r = r/cnt
    for ln in svgarr:
        arr = ln.split(" ")
        if arr[0] == "<path" and arr[1]=='d=\'M':
            
            bond_mask_cnt = bond_mask_cnt + 1
            
            tp_arr = arr[2].split(',')
            tp_arr2 = arr[4].split('\'')
            tp_arr2 = tp_arr2[0].split(',')           
            idx1 = get_closest(tp_arr, atoms_coor, r)
            idx2 = get_closest(tp_arr2, atoms_coor, r)
            # print(idx1, idx2)
            arr2 = [arr[0]] + ['id="bondMask_' + str(bond_mask_cnt) +'"'] + ['class="bondArea"'] + ['onclick=\'addBondClick(event,"'+ str(idx1) + '","' + str(idx2) +'")\''] + ['oncontextmenu=\'bondRightClick(event,"'+ str(idx1) + '","' + str(idx2) +'")\''] + arr[1:]
            n_ln = " ".join(arr2)
            pathMask_arr.append(n_ln)
            
    # print(atoms_coor)
    new_arr = new_arr + pathMask_arr + ellipse_arr
        # else:
        #     if start_append and arr[0] != "</svg>":
        #         new_arr.append(ln)
    n_svg = "\n".join(new_arr)
    return n_svg

def draw2D(sm, ifHighlight=False):
    m = Chem.MolFromSmiles(sm)
    molSize = (450, 150)                    # draw area 
    mc = Chem.Mol(m.ToBinary())    
    if not mc.GetNumConformers():
        rdd.Compute2DCoords(mc)             # compute 2D coordinates of atoms
    drawer = draw2d.MolDraw2DSVG(\
        molSize[0],molSize[1],-1,-1,True)              # initialize drawer with size
    if ifHighlight:
        drawer.DrawMolecule(mc,highlightAtoms=range(mc.GetNumAtoms()))                 # draw the molecule
    else:
        drawer.DrawMolecule(mc)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()           # get the SVG string 
    # display(SVG(svg.replace('svg:',''))) 
    return svg


def draw2DMol(m):
    # m = Chem.MolFromSmiles(sm)
    molSize = (450, 200)                    # draw area 
    mc = Chem.Mol(m.ToBinary())    
    if not mc.GetNumConformers():
        rdd.Compute2DCoords(mc)             # compute 2D coordinates of atoms
    drawer = draw2d.MolDraw2DSVG(\
        molSize[0],molSize[1],-1,-1,True)              # initialize drawer with size NO Freetype SVG
    drawer.DrawMolecule(mc,highlightAtoms=range(mc.GetNumAtoms()))                 # draw the molecule
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()           # get the SVG string 
    # display(SVG(svg.replace('svg:',''))) 
    return svg

# Inspired by: https://codeocean.com/explore/capsules?query=tag:data-curation

def generate4desc(smiles, verbose=False):

    moldata= []
    for elem in smiles:
        mol=Chem.MolFromSmiles(elem) 
        moldata.append(mol)
       
    baseData= np.arange(1,1)
    i=0  
    for mol in moldata:        
       
        desc_MolLogP = Descriptors.MolLogP(mol)
        desc_MolWt = Descriptors.MolWt(mol)
        desc_NumRotatableBonds = Descriptors.NumRotatableBonds(mol)
           
        row = np.array([desc_MolLogP,
                        desc_MolWt,
                        desc_NumRotatableBonds])   
    
        if(i==0):
            baseData=row
        else:
            baseData=np.vstack([baseData, row])
        i=i+1      
    
    columnNames=["MolLogP","MolWt","NumRotatableBonds"]   
    descriptors = pd.DataFrame(data=baseData,columns=columnNames)
    
    return descriptors

def AromaticAtoms(SMILES):
  #SMILES = 'COc1cccc2cc(C(=O)NCCCCN3CCN(c4cccc5nccnc54)CC3)oc21'
  m = Chem.MolFromSmiles(SMILES)
  aromatic_atoms = [m.GetAtomWithIdx(i).GetIsAromatic() for i in range(m.GetNumAtoms())]
  aa_count = []
  for i in aromatic_atoms:
    if i==True:
      aa_count.append(1)
  sum_aa_count = sum(aa_count)
  return sum_aa_count

def getAromaticProportion(SMILES):
  m = Chem.MolFromSmiles(SMILES)
  return AromaticAtoms(m)/Descriptors.HeavyAtomCount(m)

