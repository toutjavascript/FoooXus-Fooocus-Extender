# Made by toutjavascript.com
# https://github.com/toutjavascript/FoooXus-Fooocus-Extender



import json
import multiprocessing
import os
import html
import sys
import shutil
from gradio_client import Client
from src import api
from src import device
from src import utils
from src import sql
from src import console
from src.models import DeviceInfo, Metadata, Image
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import logging

# Constants to identify version and execution modalities
FOOOXUS_RELEASE="0.8.3"


FOOOXUS_PYINSTALLER=False 




# Check versions of module versus requirements.txt
def checkVersions(requirements):
    versions=utils.checkVersions(requirements)
    pythonVersion=utils.getPythonVersion()
    OS=utils.getOS()

    require=True

    if FOOOXUS_PYINSTALLER:
        console.printBB("You are running the [b]standalone foooxus.exe[/b] on [b]"+OS+"[/b]")
    else:
        console.printBB("You are running [b]Python V"+pythonVersion+"[/b] on [b]"+OS+"[/b]")
        if utils.in_venv():
            console.printBB(" [ok] (venv) is activated[/ok]")
        else:
            console.printBB(" [error] Carefull, (venv) is not activated. You may experience module version issues[/error]")
        console.printBB("FoooXus ckecks installed module versions and compares them to requirements.txt")

        console.printBB("  [b]Modules            Requirement       Installed version[/b]")

        for module in requirements:
            if versions[module]==requirements[module]:
                version="[ok]✔ "+versions[module]+"[/ok]"
            else:
                version="[error]X "+versions[module]+"[/error]"
                require=False
            
            console.printBB("  [b]{:<19}".format(module)+"[/b]{:<18}".format(requirements[module])+version)

        if require:
            console.printBB("[ok]All requirements are met. FoooXus should start :)[/ok]")
        else:
            console.printBB(" [error]One requirement is not met. FoooXus could fail[/error]")
    print("")

    versions["OS"]=OS
    versions["python"]=pythonVersion
    versions["PyInstaller"]=FOOOXUS_PYINSTALLER

    return versions


# Load configuration from config.json FoooXus
def loadConfig():

    requirements=utils.getRequirements("requirements.txt")

    versions=checkVersions(requirements)

    with open('config.json') as config_file:
        conf = json.load(config_file)
    if "illustrationResizeSizes" not in conf:
       conf["illustrationResizeSizes"]=[512, 512]
    if "illustrationResizeCompress" not in conf:
       conf["illustrationResizeCompress"]=80
     
    conf["illustrationsFolder"]="outputs/illustrations"
    conf["outputsFolder"]="outputs"
    conf["versions"]=versions
    conf["requirements"]=requirements
    conf["FOOOXUS_RELEASE"]=FOOOXUS_RELEASE

    # check if outputs folder exists
    utils.checkFolder(conf["outputsFolder"])
    utils.checkFolder(conf["outputsFolder"]+"/tmp")
    utils.checkFolder(conf["illustrationsFolder"]+"/models")
    utils.checkFolder(conf["illustrationsFolder"]+"/styles")
    utils.checkFolder(conf["illustrationsFolder"]+"/loras")

    conf["init"]=True  # flag to tell no api call is made yet



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




def checkInit():
    # Check if config.json not exists: run initialization
    if os.path.exists("./config.json")==False:
        console.printBB("[reverse][h1]*************************   FIRST INIT of FoooXuS APP V"+FOOOXUS_RELEASE+"   *************************[/h1][/reverse][reset]")
        console.printBB("  [ok]Thanx for using. Please report issues and ideas on[/ok] ")
        console.printBB("  [u]https://github.com/toutjavascript/FoooXus-Fooocus-Extender[/u] ")

        shutil.copy2("./templates/config.tpl", "config.json")

        console.printBB("")
        console.printBB("A new config.json has been created. Fill in these values :")
        console.printBB('"[b]fooocus-directory[/b]": "[b]C:\\Users\\TJS\\Desktop\\IA\\StabilityMatrix\\Data\\Packages\\Fooocus[/b]"')
        console.printBB('"[b]fooocus-address[/b]": "[b]127.0.0.1:7865[/b]"')
        console.printBB("")
        if FOOOXUS_PYINSTALLER:
            console.printBB("Once checked, restart [shell]foooxus.exe[/shell] ")
        else:
            console.printBB("Once checked, restart [shell]python foooxus.py[/shell] "+("or [shell]foooxus.bat[/shell] here" if utils.is_windows() else ""))
        console.printBB("")


        sys.exit("")


# STARTING FOOOXUS APP
if __name__ == '__main__':
    try:
        multiprocessing.freeze_support()
        checkInit()

        console.printBB("[reverse][h1]**********************    STARTING FoooXuS APP V"+FOOOXUS_RELEASE+"   **********************[/h1][/reverse][reset]")
        console.printBB("  [ok]Thanx for using. Please report issues and ideas on[/ok] ")
        console.printBB("  [u]https://github.com/toutjavascript/FoooXus-Fooocus-Extender[/u] ")

        conf=loadConfig()

        app = Flask(__name__)

        appPath=utils.getAppPath()

        # Prevent http flask web server logging in terminal 
        log = logging.getLogger('werkzeug')
        log.disabled = True


        console.printBB("[ok]Now, open FoooXus web UI on [u]http://"+conf["host"]+":"+str(conf["port"])+"[/u][/ok]")
        console.printBB("")

        myApi = api.FooocusApi(conf['fooocus-address']+"")


        @app.route('/')
        def home():
            return render_template('index.html', release=FOOOXUS_RELEASE)



        @app.route('/ajax/pingFoooxus', methods=['POST'])
        def pingFoooxus():
            return {"ajax":True, "ping": True, "config": conf}

        @app.route('/ajax/getDeviceInfo', methods=['POST'])
        def getDeviceInfo():
            deviceInfo=device.getDeviceInfo()
            return deviceInfo


        @app.route('/ajax/pingFooocus', methods=['POST'])
        def pingFooocus():
            ping=myApi.pingFooocus(conf["init"])
            conf["init"]=False
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

        @app.route('/ajax/sendCancel', methods=['POST'])
        def cancel():
            cancel=myApi.sendCancel()
            return json.dumps(cancel)

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
            metadata = json.loads(request.form.get('metadata', ''))
            result=myApi.sendCreateImage(metadata, uid)
            return result



        @app.route('/'+conf["illustrationsFolder"]+'/models/<filename>', methods=['GET'])
        def serveImageModel(filename):
            return send_from_directory(os.path.join(appPath, conf["illustrationsFolder"]+"/models/"), filename)

        @app.route('/'+conf["illustrationsFolder"]+'/styles/<filename>', methods=['GET'])
        def serveImageStyle(filename):
            # print(os.path.join(os.path.join(appPath, conf["illustrationsFolder"]+"/styles/"), filename))
            return send_from_directory(os.path.join(appPath, conf["illustrationsFolder"]+"/styles/"), filename)

        @app.route('/'+conf["illustrationsFolder"]+'/loras/<filename>', methods=['GET'])
        def serveImageLoral(filename):
            return send_from_directory(os.path.join(appPath, conf["illustrationsFolder"]+"/loras/"), filename)

        @app.route('/'+conf["outputsFolder"]+'/tmp/<filename>', methods=['GET'])
        def serveImage(filename):
            # print(os.path.join(os.path.join(appPath, conf["outputsFolder"]+"/tmp/"), filename))
            return send_from_directory(os.path.join(appPath, conf["outputsFolder"]+"/tmp/"), filename)

        @app.route('/favicon.ico', methods=['GET'])
        def serveFavicon():
            return send_from_directory(os.path.join(appPath, 'static/picto'), 'favicon.ico',mimetype='image/vnd.microsoft.icon')



        app.run(host=conf['host'], port=conf['port'])
    except SystemExit as e:
        print("")
        #print("FoooXus emits exception ", e)
