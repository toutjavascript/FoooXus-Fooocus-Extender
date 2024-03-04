# FoooXus: Fooocus Extender

## What is it for?
FoooXus uses **Fooocus Gradio API** to extend Fooocus functionnalities :
- Manage your Styles, Models and LoRAs with preset prompts
- Simply add or remove presets in config.json file
- View all your images presets
- Launch image creation works to a queue that is processed in background
- Create generation batches with variations on some parameters (not ready yet)

![How it looks](https://github.com/toutjavascript/FoooXus-Fooocus-Extender/assets/30899600/9629f7d0-a710-4e2d-a698-4290d45f71a7)

## Prerequisites
You need a running Fooocus instance to use FoooXus.
You must install FoooXus on the same device than Fooocus.

## Use the standalone foooxus.exe
[See this document to use foooxus.exe executable](executable.md)

## How to install without running the .exe
Natively, FoooXus is a python app server that launches a web UI and connect to Fooocus via API
Install FoooXus following these standard steps.

```
# Get the sources 
git clone https://github.com/toutjavascript/FoooXus-Fooocus-Extender.git
cd FoooXus-Fooocus-Extender

# Activate the virtual python environment
python -m venv venv
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# First run of the FoooXus app to initialize
python foooxus.py
```

Terminal will show this kind of message
![Init of app](https://github.com/toutjavascript/FoooXus-Fooocus-Extender/assets/30899600/1c16d3e7-b0af-48cf-920c-2a04c893ef01)

Fill in the fields in config.json file

FoooXus is now ready to start with a new call to
```
python foooxus.py
```


## How to use every day
On Windows, you can double-click <code>foooxus.bat</code>

Or if you prefer
```
# Check you are in your (venv) virtual environment
# if not, activate it
venv\Scripts\activate

# Run the FoooXus app
python foooxus.py
```

Terminal shows now versions and much more informations to understand what happens
![FoooXus starts](https://github.com/toutjavascript/FoooXus-Fooocus-Extender/assets/30899600/2eda20a1-3f10-46a9-b5bc-531674226d28)

Open your browser on http://127.0.0.1:7878 to view FoooXus UI

## How to update FoooXus
To update FoooXus from this github repository, open a terminal in your FoooXus-Fooocus-Extender 
```
git pull
```

## Updates on Fooocus
- Fooocus could be updated at every moment. It could broke the API.
- FoooXus version is tested with V2.2.1 Fooocus Release.

## History Log
V0.9.0 Adapt to Gradio API to Fooocus 2.2.1

V0.8.3 Fix issue on macOS https://github.com/toutjavascript/FoooXus-Fooocus-Extender/issues/5

V0.8.2 Add a button to clear queue 

V0.8.1 Improve the error messages 

V0.8 New standalone fooocus.exe 
- new config.json options 
- download the fooocus.exe executable file to avoid tedious python, git, pip installations

V0.6 Updates on install process
- If you have issues, please tell me, with a copy of a terminal

V0.5 Very First release
- Please, tell me if it is broken somewhere
- Please, share your ideas by opening new discussions

## Some functionnalities
Get notified when new image is generated
![Notifications](https://github.com/toutjavascript/FoooXus-Fooocus-Extender/assets/30899600/96146dca-fd97-4729-b7e4-0fd2699580c6)

View history 
![Queue and history](https://github.com/toutjavascript/FoooXus-Fooocus-Extender/assets/30899600/e82f3b8b-db2c-41b4-9f21-29fb315960e5)

Python terminal shows all generations
![Terminal shows generation log](https://github.com/toutjavascript/FoooXus-Fooocus-Extender/assets/30899600/3d9190f8-e730-4893-8e9f-dda637419778)
