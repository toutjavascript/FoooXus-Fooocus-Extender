function viewHelpConfigPreset() {
    var converter = new showdown.Converter();
    var text      = `
## How to manage illustration presets in config.json

After the first lines of "config.json" file, dedicated to general configuration, you will find the 3 parts of illustration presets.

First one is the preset arrays of **style-illustrations**. 

Each element defines a preset with :
    
    {
        "name": "s1",
        "description": "Illustration #1 for all styles, A cat",
        "metadata": {
            "Base Model": "juggernautXL_v8Rundiffusion.safetensors",foooxusQueue
            "Prompt": "A cat",
            "Seed": "314159"
        }           
    },

A preset contains :
- a name
- a description
- a metadata object that describes how the picture must be generated


Metadata part may contain that parameters :
    
    {
        "name": "s1",
        "description": "Illustration #1 for all styles, A cat",
        "metadata": {
            "Base Model": "juggernautXL_v8Rundiffusion.safetensors",
            "Prompt": "A cat",
            "Seed": "314159",
            "ADM Guidance": "(1.5, 0.8, 0.3)",
            "Sampler": "dpmpp_2m_sde_gpu",
            "Scheduler": "karras",
            "Performance": "Quality",
            "Sharpness": 5,
            "Guidance Scale": 2,
            "Refiner Model": "juggernautXL_v8Rundiffusion.safetensors",
            "Refiner Switch": 0.5,
            "Lora 1": "sd_xl_offset_example",
            "Weight Lora 1": 1
        }    
    },

Add, edit or remove presets as you like.

**You must restart FoooXus app to take into account these file updates**

Models and Loras presets below in the file are similar
    
    
    `
    
    
    openHelpModal(converter.makeHtml(text))
}



function viewHelpConfigFile() {
    var converter = new showdown.Converter();
    var text      = `
## How to fill in config.json
"config.json" file is auto generated at first launch with a template.
You must configure it with two important values:

1- **fooocus-directory** contains the full path of your Fooocus installation
Note that you **MUST** double the "\\\\" in each folder 

2- **fooocus-address** contains the http address of Fooocus web UI.
By default, the address is "127.0.0.1:7865" and should work

**You must restart FoooXus app to take into account these file updates**

The next part of "config.json" file is dedicated to illustration presets.
    `
    
    
    openHelpModal(converter.makeHtml(text))

}


function openHelpModal(html) {
    var myModal = new jBox('Modal', {
        content: html
    });       
    myModal.open();

}