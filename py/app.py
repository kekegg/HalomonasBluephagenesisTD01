from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from xml.dom import minidom
import json
from flask import jsonify
import hashlib
import pandas as pd
import rdkit.Chem.Draw
from rdkit import Chem

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app) #, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/molapi', methods=['POST'])
def molapi():
    if request.method == 'POST':
        res = request.get_json()
        print(res)
        fl_path = 'flaskr' + res['img_url']
        dt = pd.read_csv(fl_path)
        print(dt.shape)

@app.route('/smiles', methods=('GET', 'POST'))
def apismiles():
    if request.method == 'POST':
        res = request.get_json()
        #print(request)
        meta_dt = pd.read_csv('./TD01_meta.csv')
        meta_dt = meta_dt.set_index('Metabolite Name')
        #print(meta_dt[:5])
        #print("For debug")
        #print(res['molname'])
        smi = meta_dt.loc[res['molname'],'Smiles']
        #print(smi)
        mol = Chem.MolFromSmiles(smi)
        #print(mol)
        rnd_str = hashlib.md5(res['molname'].encode())  #get_random_string(8)
        file_path = "static/images/"+ rnd_str.hexdigest() +".png"
        src_path = "http://localhost:5000/static/images/" + rnd_str.hexdigest() + ".png"
        if mol:
            Chem.Draw.MolToFile(mol, file_path)
            print("draw smiles")

            return src_path
        else:
            return ""

@app.route('/api', methods=['GET'])
def api():
    doc = minidom.parse('../CoreHuangPlain.svg')
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
            print(path.childNodes[0].nodeValue)
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
    return jsonify(dt)

@app.route('/test', methods=['GET'])
def test():
    return render_template('meta.html')


if __name__ == '__main__':
    app.run()
