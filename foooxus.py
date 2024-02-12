import json
import os
import html
import timeit
from gradio_client import Client
from src import api
from src import device
from src import utils
from src import sql
from src.models import DeviceInfo, Metadata, Image
from flask import Flask, render_template, request, redirect, url_for, send_from_directory


# Load configuration from config.json FoooXus
def loadConfig():
    with open('config.json') as config_file:
        conf = json.load(config_file)
    conf["illustrationsFolder"]="outputs/illustrations"
    conf["outputsFolder"]="outputs"

    # check if outputs folder exists
    utils.checkFolder(conf["outputsFolder"])
    utils.checkFolder(conf["outputsFolder"]+"/tmp")
    utils.checkFolder(conf["illustrationsFolder"]+"/models")
    utils.checkFolder(conf["illustrationsFolder"]+"/styles")
    utils.checkFolder(conf["illustrationsFolder"]+"/loras")

    # check if database exists
    # sql.connect()
    # TODO later

    conf["fooocusConfig"]=loadFooocusConfig(conf["fooocus-directory"])

    if conf["fooocusConfig"]:
        conf["messageConfig"]=""
        conf["loras-directory"]=conf["fooocusConfig"]["path_loras"]
    else:
        conf["messageConfig"]="<b>'fooocus-directory'</b> parameter in config.json is not correct.<br>No Fooocus install found in this folder:<br>"+html.escape(conf["fooocus-directory"])

    return conf

# Load the config.txt Fooocus file 
def loadFooocusConfig(dir):
    try:
        with open(os.path.join(dir, "config.txt")) as config_file:
            fooocusConfig = json.load(config_file)
    except:
        fooocusConfig = False

    return fooocusConfig




conf=loadConfig()



app = Flask(__name__)
myApi = api.FooocusApi(conf['fooocus-address']+"")


@app.route('/')
def home():
    return render_template('index.html')



@app.route('/ajax/pingFoooxus', methods=['POST'])
def pingFoooxus():
    return {"ajax":True, "ping": True, "config": conf}



@app.route('/ajax/getDeviceInfo', methods=['POST'])
def getDeviceInfo():
    deviceInfo=device.getDeviceInfo()
    return deviceInfo


@app.route('/ajax/pingFooocus', methods=['POST'])
def pingFooocus():
    ping=myApi.pingFooocus()
    return ping

@app.route('/ajax/getModels', methods=['POST'])
def getModels():
    models=myApi.getModels()
    return json.dumps(models)

@app.route('/ajax/getStyles', methods=['POST'])
def getStyles():
    models=myApi.getStyles()
    return json.dumps(models)

@app.route('/ajax/getLoras', methods=['POST'])
def getLoras():
    loras=myApi.getLoras(conf["loras-directory"])
    return json.dumps(loras)

@app.route('/ajax/getConfig', methods=['POST'])
def getConfig():
    conf["ajax"]=True
    return conf

@app.route('/ajax/getIllustrations', methods=['POST'])
def getIllustrations():
    result={"illustrations":{}}
    result["illustrations"]["models"]=utils.getFiles(conf["illustrationsFolder"]+"/models", "jpg")
    result["illustrations"]["styles"]=utils.getFiles(conf["illustrationsFolder"]+"/styles", "jpg")
    result["illustrations"]["loras"]=utils.getFiles(conf["illustrationsFolder"]+"/loras", "jpg")
    return json.dumps(result)

@app.route('/ajax/generateImage', methods=['POST'])
def generateImage():
    uid = request.form.get('uid', '') 
    print("uid = "+uid)
    metadata = json.loads(request.form.get('metadata', ''))

    print("typeof(metadata) = ", type(metadata))
    print("metadata = ",metadata)
    result=myApi.sendCreateImage(metadata, uid)
    return result



@app.route('/'+conf["illustrationsFolder"]+'/models/<filename>', methods=['GET'])
def serveImageModel(filename):
    return send_from_directory(conf["illustrationsFolder"]+"/models/", filename)

@app.route('/'+conf["illustrationsFolder"]+'/styles/<filename>', methods=['GET'])
def serveImageStyle(filename):
    return send_from_directory(conf["illustrationsFolder"]+"/styles/", filename)

@app.route('/'+conf["illustrationsFolder"]+'/loras/<filename>', methods=['GET'])
def serveImageLoral(filename):
    return send_from_directory(conf["illustrationsFolder"]+"/loras/", filename)

@app.route('/'+conf["outputsFolder"]+'/tmp/<filename>', methods=['GET'])
def serveImage(filename):
    return send_from_directory(conf["outputsFolder"]+"/tmp", filename)

@app.route('/favicon.ico', methods=['GET'])
def serveFavicon():
    return send_from_directory(os.path.join(app.root_path, 'static/picto'), 'favicon.ico',mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host=conf['host'], port=conf['port'])
