
from xml.dom import minidom
import json
import hashlib
import pandas as pd
import rdkit.Chem.Draw
from rdkit import Chem

from mol_basic import draw2D, draw2DMol, modify_svg
from tdmeta.ttypes import mapOptions

#draggable="true" ondragstart="onDragStart(event)" ondragend="onDragEnd(event)"
class Tdmeta():
    def __init__(self):
        meta_dt = pd.read_csv('py/data/TD01_meta.csv')
        meta_dt = meta_dt.set_index('Metabolite Name')
        self.meta_dt = meta_dt
        self.svg_base = """<svg id="svgMap"  width="2363.8844mm"
   height="3672.0916mm"
   viewBox="-500 -500 1863.8844 2672.0915" 
   version="1.1"
   inkscape:version="1.2-dev (9ee32be, 2021-06-19)"
   sodipodi:docname="CoreHuangPlain2.svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   """
        self.svg_def = """
<defs
     id="defs22468">
    <marker
       style="overflow:visible"
       refY="0"
       refX="0"
       orient="auto"
       id="Arrow1Lstart">
      <path
         
         transform="matrix(0.8,0,0,0.8,3,0)"
         style="fill-rule:evenodd;stroke:#000000;stroke-width:1.00000003pt;marker-start:none"
         id="path_arrowstart-26"
         d="M 0,0 1.5,-1.5 -3.75,0 1.5,1.5 Z" />
    </marker>
    <marker
       style="overflow:visible"
       refY="0"
       refX="0"
       orient="auto"
       id="Arrow1Lend">
      <path
        
         transform="matrix(-0.8,0,0,-0.8,-3,0)"
         style="fill-rule:evenodd;stroke:#000000;stroke-width:1.00000003pt;marker-start:none"
         id="path_arrowend-88"
         d="M 0,0 1.5,-1.5 -3.75,0 1.5,1.5 Z" />
    </marker>
  </defs>
  """
    def test1(self, typ):
        x = np.arange(512)      
        print(typ)
        if typ:
            x = x*x + 5*x + 6 * x*x*x
            return x.tolist()
        else:
            x = np.sin(0.05*x)
            return x.tolist()

    def getMapData(self, opt):
        doc = minidom.parse('py/data/CoreHuangPlain2.svg')
        dt = dict()
        dt['path'] = []
        for path in doc.getElementsByTagName('path'):
            cur = dict()
            cur['d'] = path.getAttribute('d')
            cur['id'] = path.getAttribute('id')
            cur['style'] = path.getAttribute('style')
            dt['path'].append(cur)

        dt['text'] = []
        for path in doc.getElementsByTagName('text'):
            cur = dict()
            cur['id'] = path.getAttribute('id')
            cur['y'] = path.getAttribute('y')
            cur['x'] = path.getAttribute('x')
            cur['style'] = path.getAttribute('style')
    #cur['data'] = path.childNodes[0].nodeValue
    #dt['text'].append(cur)
            try:
                cur['data'] = path.childNodes[0].nodeValue
                # print(path.childNodes[0].nodeValue)
                dt['text'].append(cur)
            except:
                print("")
        dt['circle'] = []
        for path in doc.getElementsByTagName('circle'):
            cur = dict()
            cur['id'] = path.getAttribute('id')
            cur['r'] = path.getAttribute('r')
            cur['cy'] = path.getAttribute('cy')
            cur['cx'] = path.getAttribute('cx')
            cur['style'] = path.getAttribute('style')
            cur['transform'] = path.getAttribute('transform')
            dt['circle'].append(cur)
        
        path_dic = dt['path']
        svg_str = self.svg_base

        print(opt.zoomScale)
        svg_str +=  f"transform=\"translate(0,0) scale({opt.zoomScale})\">"
        svg_str += self.svg_def
        for pth in path_dic:
            # print(pth['id'])
            if opt.zoomScale < 0.11:
                stl = pth['style']
                stl = stl.replace("stroke-width:0.529167;", "stroke-width:1.0;")
                svg_str += "<path class=\"reac_path\" id=\"" + pth['id'] + "\" d=\"" + pth['d'] + "\" style=\"" + stl + "\"/>\n"
            else:
                svg_str += "<path class=\"reac_path\" id=\"" + pth['id'] + "\" d=\"" + pth['d'] + "\" style=\"" + pth['style'] + "\"/>\n"
        for pth in dt['text']:
            try:
                svg_str += "<text class=\"svg_text\" id=\"" + pth['id'] + "\" y=\"" + pth['y'] + "\" x=\"" + pth['x'] + "\" style=\"" + pth['style'] + "\" onclick=\"textClick(event, '" + pth['data'] + "')\">" + pth['data'] + "</text>\n"
            except:
                continue
        for pth in dt['circle']:
            svg_str += "<circle class=\"metabolite\" id=\"" + pth['id'] + "\" cy=\"" + pth['cy'] + "\" cx=\"" + pth['cx'] + "\" r=\"" + pth['r'] + "\" transform=\"" + pth['transform'] + "\" style=\"" + pth['style'] + "\"/>\n"

        svg_str += "</svg>"
        f = open('test.svg', 'w')
        f.write(svg_str)
        f.close()
        return svg_str


    def drawSmiles(self, meta_name):

        smi = self.meta_dt.loc[meta_name,'Smiles']
        print(smi)
        # mol = Chem.MolFromSmiles(smi)
        # print(mol)
        svg = draw2D(smi)
        # new_svg = modify_svg(svg)
        return svg
        
