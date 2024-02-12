# FoooXus: Fooocus Extender

## What is it for?
FoooXus uses **Fooocus Gradio API** to extend Fooocus functionnalities :
- Manage your Styles, Models and LoRAs with preset prompts
- Simply add or remove presets in config.json file
- View all your images presets
- Launch image creation works to a queue that is processed in background
- Create generation batches with variations on some parameters (not ready yet)

## How to install
FoooXus is a python app server that launches a web UI and connect to Fooocus via API
You need a running Fooocus instance to use FoooXus.
You must install FoooXus on the same device than Fooocus.

```
# Get the sources 
git clone FoooXus-Fooocus-Extender
cd FoooXus-Fooocus-Extender

# Activate the virtual python environment
python -m venv venv
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Edit the config.json file and fill in the fooocus install directory and check the fooocus directory and path
    "host": "127.0.0.1",        
    "port": 7878,
    "fooocus-directory": "C:\\Users\\lannister\\Desktop\\IA\\StabilityMatrix\\Data\\Packages\\Fooocus",
    "fooocus-address": "127.0.0.1:7865",
```
FoooXus is now ready to start.

## How to use
```
# Check you are in your (venv) virtual environment
# if not, activate it
python -m venv venv
venv\Scripts\activate

# Run the FoooXus app
python foooxus.py
```

Open your browser on http://127.0.0.1:7878 to view FoooXus UI

## Updates on Fooocus
Fooocus could be updated at every moment. It could broke the API.
FoooXus version is tested with V2.1.865 Fooocus Release.


## History Log
V0.5 Very First release
Please, tell me if it is broken somewhere
Please, share your ideas by opening new discussions


