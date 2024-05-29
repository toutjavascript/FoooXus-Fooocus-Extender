import os
import shutil
import traceback
import timeit
from datetime import datetime
import sys
from src import utils
from src import console
from gradio_client import Client


class ConfigApi:
    def __init__(self):
        self.ping=11
        self.cancel=0
        self.init=35
        self.generate=46
        self.models=32
        self.styles=21
        self.checkDelta=False
        self.delta=0
        self.deltaPing=0
        self.deltaCancel=0
        self.deltaInit=0
        self.deltaGenerate=0
        self.deltaModels=0
        self.deltaStyles=0


class FooocusApi:
    def __init__(self, base_url, outputFolder, FOOOCUS_MIN_RELEASE):
        self.FOOOCUS_MIN_RELEASE=FOOOCUS_MIN_RELEASE
        self.config=ConfigApi()
        self.client=None
        self.outputFolder=outputFolder
        if base_url[0:7] != "http://"[0:7]:
            base_url="http://"+base_url
        self.base_url = base_url.strip()
        self.emptyImage="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg=="

    def getClient(self):
        if (self.client==None):
            # print("Open API client to Fooocus instance at "+self.base_url+" ...")
            try:
                self.client = Client(self.base_url, serialize=False)
                console.printBB("[ok]Great! FoooXus is now connected to Fooocus[/ok]")
                return self.client
            except Exception as e:
                self.client=None
                console.printBB("[error]Connection to Fooocus failed...[/error]")
                exceptionName=type(e).__name__
                if exceptionName=="ConnectionError":
                    console.printBB("[error] ConnectionError, check that:[/error]")
                    console.printBB("[error]  - Fooocus must be running, on the same device[/error]")
                    console.printBB("[error]  - Fooocus address config.json is set to "+self.base_url+" [/error]")
                else:
                    console.printBB("[error] "+exceptionName+"[/error]")

                print(f"{e}")
                print("")
                return None
        else:
            return self.client


    # Ping Fooocus instance 
    def pingFooocus(self, firstCall=False):
        try:
            client=self.getClient()
            if(client is None):
                # Not connected, so no call to predict
                return {"ajax":True, "error":True}
           
            result = client.predict( fn_index=self.config.ping+self.config.deltaPing )
            if firstCall:
                console.printBB("[ok]FoooXus is connected to Fooocus. Let's play in the web UI ![/ok]")
            return {"ajax":True, "error":False, "ping":True, "fooocusUrl": self.base_url}
        except Exception as e:
            if self.config.deltaPing<=10:
                console.printBB("[warning]pingFooocus() failed. Trying to find the right gradio API fn_index ("+str(self.config.ping)+"+"+str(self.config.deltaPing)+")[/warning]")
                self.config.deltaPing+=1
                #self.config.deltaInit+=1
                #self.config.deltaGenerate+=1
                #self.config.deltaCancel+=1
                #self.config.deltaStyles+=1
                self.config.deltaModels+=1
                return self.pingFooocus(firstCall)
            else:
                console.printExceptionError(e)
                console.printBB("[error]FoooXus is not connected to Fooocus gradio API :([/error]")
                console.printBB("[error] - Fooocus must be running, on the same device[/error]")
                console.printBB("[error] - Fooocus must be at least "+self.FOOOCUS_MIN_RELEASE+"[/error]")
                console.printBB("[error] - If FoooXus app has already worked, Fooocus may have changed version.[/error]")
                console.printBB("[error]   it may break API calls[/error]")
                console.printBB("")
                return {"ajax":True, "error":True}
    
    # Cancel generation
    def sendCancel(self):
        try:      
            console.printBB("[b] /!\ You have canceled the queue[/b]")
            console.printBB("[b] [/b]")
            result = self.getClient().predict( fn_index=self.config.cancel )
            return {"ajax":True, "error":False}
        except Exception as e:
            console.printExceptionError(e)
            return {"ajax":True, "error":True}
        

    # Get list of all models installed on the Fooocus folder
    def getModels(self):
        try:
            result = self.getClient().predict( fn_index=self.config.models+self.config.deltaModels )
            models=[]
            if (result[0]):
                if (result[0]["choices"]):
                    for model in result[0]["choices"]:
                        models.append(model)
            return {"ajax":True, "error":False, "models":models}
        except Exception as e:
            if self.config.deltaModels<10:
                console.printBB("[warning]getModels() failed. Trying to find the right gradio API fn_index (i+"+str(self.config.deltaModels)+")[/warning]")
                self.config.deltaModels+=1
                self.config.deltaInit+=1
                self.config.deltaGenerate+=1
                return self.getModels()
            else:
                print("[error] getModels exception[/error]") 
                print(f"Error: {e}")
                return {"ajax":True, "error":True}


    # Get all styles available for Fooocus
    def getStyles(self):
        try:
            result = self.getClient().predict( [], fn_index=self.config.styles+self.config.deltaStyles )
            styles=[]
            if ("choices" in result):
                for style in result["choices"]:
                    if style[0]!="Random Style":
                        styles.append(style[0])
            return {"ajax":True, "error":False, "styles":styles}
        except:
            if self.config.deltaStyles<10:
                console.printBB("[warning]getStyles() failed. Trying to find the right gradio API fn_index (i+"+str(self.config.deltaStyles)+")[/warning]")
                self.config.deltaStyles+=1
                self.config.deltaModels+=1
                self.config.deltaInit+=1
                self.config.deltaGenerate+=1
                return self.getStyles()
            else:
                return {"ajax":True, "error":True}

    # Get all Loras from the loras-directory
    def getLoras(self, dir):
        try:
            loras=utils.getFiles(dir, ".safetensors")
            return {"ajax":True, "error":False, "loras":loras}
        except:
            return {"ajax":True, "error":True}
            

    # InitFooocus does not exist since Fooocus V2.2.1. All parameters in CreateImage
    def initFooocus(self, metadata={}):

        return False

        try:
            adm=metadata.get("ADM Guidance").replace("(","").replace(")","")
            admSplit=adm.split(", ")
            result = self.getClient().predict( 
				True,	# bool in 'Disable Preview' Checkbox component
				float(admSplit[0]),	# int | float (numeric value between 0.1 and 3.0)							in 'Positive ADM Guidance Scaler' Slider component
				float(admSplit[1]),	# int | float (numeric value between 0.1 and 3.0)							in 'Negative ADM Guidance Scaler' Slider component
				float(admSplit[2]),	# int | float (numeric value between 0.0 and 1.0)							in 'ADM Guidance End At Step' Slider component
				7,	# int | float (numeric value between 1.0 and 30.0)								in 'CFG Mimicking from TSNR' Slider component
				metadata["Sampler"],	# str (Option from: ['euler', 'euler_ancestral', 'heun', 'heunpp2', 'dpm_2', 'dpm_2_ancestral', 'lms', 'dpm_fast', 'dpm_adaptive', 'dpmpp_2s_ancestral', 'dpmpp_sde', 'dpmpp_sde_gpu', 'dpmpp_2m', 'dpmpp_2m_sde', 'dpmpp_2m_sde_gpu', 'dpmpp_3m_sde', 'dpmpp_3m_sde_gpu', 'ddpm', 'lcm', 'ddim', 'uni_pc', 'uni_pc_bh2'])								in 'Sampler' Dropdown component
				metadata["Scheduler"],	# str (Option from: ['normal', 'karras', 'exponential', 'sgm_uniform', 'simple', 'ddim_uniform', 'lcm', 'turbo']) 								in 'Scheduler' Dropdown component
				False,	# bool in 'Generate Image Grid for Each Batch' Checkbox component
				-1,	# int | float (numeric value between -1 and 200)								in 'Forced Overwrite of Sampling Step' Slider component
				-1,	# int | float (numeric value between -1 and 200)								in 'Forced Overwrite of Refiner Switch Step' Slider component
				-1,	# int | float (numeric value between -1 and 2048)								in 'Forced Overwrite of Generating Width' Slider component
				-1,	# int | float (numeric value between -1 and 2048)								in 'Forced Overwrite of Generating Height' Slider component
				-1,	# int | float (numeric value between -1 and 1.0)								in 'Forced Overwrite of Denoising Strength of "Vary"' Slider component
				-1,	# int | float (numeric value between -1 and 1.0)								in 'Forced Overwrite of Denoising Strength of "Upscale"' Slider component
				False,	# bool in 'Mixing Image Prompt and Vary/Upscale' Checkbox component
				False,	# bool in 'Mixing Image Prompt and Inpaint' Checkbox component
				False,	# bool in 'Debug Preprocessors' Checkbox component
				False,	# bool in 'Skip Preprocessors' Checkbox component
				0,	# int | float (numeric value between 0.0 and 1.0)							in 'Softness of ControlNet' Slider component
				1,	# int | float (numeric value between 1 and 255)								in 'Canny Low Threshold' Slider component
				1,	# int | float (numeric value between 1 and 255)								in 'Canny High Threshold' Slider component
				"joint",	# str (Option from: ['joint', 'separate', 'vae'])					in 'Refiner swap method' Dropdown component
				False,	# bool in 'Enabled' Checkbox component
				0,	# int | float (numeric value between 0 and 2)								in 'B1' Slider component
				0,	# int | float (numeric value between 0 and 2)								in 'B2' Slider component
				0,	# int | float (numeric value between 0 and 4)								in 'S1' Slider component
				0,	# int | float (numeric value between 0 and 4)								in 'S2' Slider component
				False,	# bool in 'Debug Inpaint Preprocessing' Checkbox component
				False,	# bool in 'Disable initial latent in inpaint' Checkbox component
				"None",	# str (Option from: ['None', 'v1', 'v2.5', 'v2.6'])								in 'Inpaint Engine' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)								in 'Inpaint Denoising Strength' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)								in 'Inpaint Respective Field' Slider component
				False,	# bool in 'Enable Mask Upload' Checkbox component
				False,	# bool in 'Invert Mask' Checkbox component
				-64,	# int | float (numeric value between -64 and 64)								in 'Mask Erode or Dilate' Slider component
				fn_index=self.config.init+self.config.deltaInit
            )
            return {"ajax":True, "error":False, "init":True}
        except Exception as e:
            if self.config.deltaInit<10:
                console.printBB("[warning]initFooocus() failed. Trying to find the right gradio API fn_index (i+"+str(self.config.deltaInit)+")[/warning]")
                self.config.deltaInit+=1
                self.config.deltaGenerate+=1
                return self.initFooocus(metadata)
            else:
                print("getModels exception")
                print(f"Error: {e}")
                return {"ajax":True, "error":True}



    def sendCreateImage(self, metadata, uid):
        try:
            adm=metadata.get("ADM Guidance").replace("(","").replace(")","")
            admSplit=adm.split(", ")
            start_time = timeit.default_timer()
            # self.initFooocus(metadata) # not present in Fooocus V2.2.1

            # Check Turbo or Lighting models



            now = datetime.now()
            console.printBB("[hour]"+now.strftime("%H:%M:%S")+"[/hour] [b]#"+uid+"[/b] New generation asked and sent to Fooocus")
            console.printBB("          [fade]Prompt:[/fade] "+metadata["Prompt"])
            console.printBB("          [fade]Model:[/fade]  "+metadata["Base Model"])
            performance=metadata["Performance"]
            if "lightning" in metadata["Base Model"].lower():
                console.printBB("          [fade]Lightning model:[/fade] "+"Force to Lightning Performance")
                performance="Lightning"

            if "turbo" in metadata["Base Model"].lower():    
                console.printBB("          [fade]Turbo model:[/fade] "+"Force to Extreme Speed Performance")
                performance="Extreme Speed"
            console.printBB("          [fade]Styles:[/fade] "+"," .join(str(s) for s in metadata["Styles"]))


            result = self.getClient().predict( 
                False,	                    # bool in 'Generate Image Grid for Each Batch' Checkbox component
                metadata["Prompt"],	        # str in 'parameter_10' Textbox component
                metadata["Negative Prompt"],# str in 'Negative Prompt' Textbox component
                metadata["Styles"],	        # List[str] in 'Selected Styles' Checkboxgroup component
                performance,	            # str in 'Performance' Radio component
                '1024×1024',	            # str in 'Aspect Ratios' Radio component
                1,	                        # int | float (numeric value between 1 and 64)	in 'Image Number' Slider component
                "png",	                    # str in 'Output Format' Radio component
                metadata["Seed"],	        # str in 'Seed' Textbox component
                True,                   	# bool in 'Read wildcards in order' Checkbox component
                metadata["Sharpness"],	    # int | float (numeric value between 0.0 and 30.0)	in 'Image Sharpness' Slider component
                metadata["Guidance Scale"],	# int | float (numeric value between 1.0 and 30.0)	in 'Guidance Scale' Slider component
                metadata["Base Model"], 	# str 	in 'Base Model (SDXL only)' Dropdown component
                metadata["Refiner Model"],	# str 	in 'Refiner (SDXL or SD 1.5)' Dropdown component
                metadata["Refiner Switch"],	# int | float (numeric value between 0.1 and 1.0)	in 'Refiner Switch At' Slider component
				True,	                    # bool in 'Enable' Checkbox component 
                metadata["Lora 1"],	        # str 	in 'LoRA 1' Dropdown component
                metadata["Weight Lora 1"],	# int | float (numeric value between -2 and 2)		in 'Weight' Slider component
				True,	                    # bool in 'Enable' Checkbox component 
                metadata["Lora 2"],	        # str 	in 'LoRA 2' Dropdown component
                metadata["Weight Lora 2"],	# int | float (numeric value between -2 and 2)		in 'Weight' Slider component
				True,	                    # bool in 'Enable' Checkbox component 
                metadata["Lora 3"],	        # str 	in 'LoRA 3' Dropdown component
                metadata["Weight Lora 3"],	# int | float (numeric value between -2 and 2)		in 'Weight' Slider component
				True,	                    # bool in 'Enable' Checkbox component 
                metadata["Lora 4"],	        # str 	in 'LoRA 4' Dropdown component
                metadata["Weight Lora 4"],	# int | float (numeric value between -2 and 2)		in 'Weight' Slider component
				True,	                    # bool in 'Enable' Checkbox component 
                metadata["Lora 5"],	        # str 	in 'LoRA 5' Dropdown component
                metadata["Weight Lora 5"],	# int | float (numeric value between -2 and 2)		in 'Weight' Slider component
				True,	# bool in 'Input Image' Checkbox component
				"Howdy!",	# str in 'parameter_91' Textbox component
				"Disabled",	# str in 'Upscale or Variation:' Radio component
				self.emptyImage,	# str (filepath or URL to image)								in 'Drag above image to here' Image component
				["Left"],	# List[str] in 'Outpaint Direction' Checkboxgroup component
				self.emptyImage,	# str (filepath or URL to image)								in 'Drag inpaint or outpaint image to here' Image component
				"Howdy!",	# str in 'Inpaint Additional Prompt' Textbox component
				self.emptyImage,	# str (filepath or URL to image)								in 'Mask Upload' Image component
				True,	# bool in 'Disable Preview' Checkbox component
				True,	# bool in 'Disable Intermediate Results' Checkbox component
				True,	# bool in 'Disable seed increment' Checkbox component
				True,	# bool in 'Black Out NSFW' Checkbox component
				float(admSplit[0]),	# int | float (numeric value between 0.1 and 3.0)							in 'Positive ADM Guidance Scaler' Slider component
				float(admSplit[1]),	# int | float (numeric value between 0.1 and 3.0)							in 'Negative ADM Guidance Scaler' Slider component
				float(admSplit[2]),	# int | float (numeric value between 0.0 and 1.0)							in 'ADM Guidance End At Step' Slider component
				7,	# int | float (numeric value between 1.0 and 30.0)	in 'CFG Mimicking from TSNR' Slider component
				1,	# int | float (numeric value between 1 and 12)  'CLIP Skip' Slider component
				metadata["Sampler"],	# str (Option from: ['euler', 'euler_ancestral', 'heun', 'heunpp2', 'dpm_2', 'dpm_2_ancestral', 'lms', 'dpm_fast', 'dpm_adaptive', 'dpmpp_2s_ancestral', 'dpmpp_sde', 'dpmpp_sde_gpu', 'dpmpp_2m', 'dpmpp_2m_sde', 'dpmpp_2m_sde_gpu', 'dpmpp_3m_sde', 'dpmpp_3m_sde_gpu', 'ddpm', 'lcm', 'ddim', 'uni_pc', 'uni_pc_bh2'])								in 'Sampler' Dropdown component
				metadata["Scheduler"],	# str (Option from: ['normal', 'karras', 'exponential', 'sgm_uniform', 'simple', 'ddim_uniform', 'lcm', 'turbo']) 								in 'Scheduler' Dropdown component
				"Default (model)",	# str (Option from: ['Default (model)'])  'VAE' Dropdown component
				-1,	# int | float (numeric value between -1 and 200)	in 'Forced Overwrite of Sampling Step' Slider component
				-1,	# int | float (numeric value between -1 and 200)	in 'Forced Overwrite of Refiner Switch Step' Slider component
				-1,	# int | float (numeric value between -1 and 2048)	in 'Forced Overwrite of Generating Width' Slider component
				-1,	# int | float (numeric value between -1 and 2048)	in 'Forced Overwrite of Generating Height' Slider component
				-1,	# int | float (numeric value between -1 and 1.0)	in 'Forced Overwrite of Denoising Strength of "Vary"' Slider component
				-1,	# int | float (numeric value between -1 and 1.0)	in 'Forced Overwrite of Denoising Strength of "Upscale"' Slider component
				False,	# bool in 'Mixing Image Prompt and Vary/Upscale' Checkbox component
				False,	# bool in 'Mixing Image Prompt and Inpaint' Checkbox component
				False,	# bool in 'Debug Preprocessors' Checkbox component
				False,	# bool in 'Skip Preprocessors' Checkbox component
				1,	# int | float (numeric value between 1 and 255)								in 'Canny Low Threshold' Slider component
				1,	# int | float (numeric value between 1 and 255)								in 'Canny High Threshold' Slider component
				"joint",	# str (Option from: ['joint', 'separate', 'vae'])					in 'Refiner swap method' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)							in 'Softness of ControlNet' Slider component
				False,	# bool in 'Enabled' Checkbox component
				0,	# int | float (numeric value between 0 and 2)								in 'B1' Slider component
				0,	# int | float (numeric value between 0 and 2)								in 'B2' Slider component
				0,	# int | float (numeric value between 0 and 4)								in 'S1' Slider component
				0,	# int | float (numeric value between 0 and 4)								in 'S2' Slider component
				False,	# bool in 'Debug Inpaint Preprocessing' Checkbox component
				False,	# bool in 'Disable initial latent in inpaint' Checkbox component
				"None",	# str (Option from: ['None', 'v1', 'v2.5', 'v2.6'])								in 'Inpaint Engine' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)								in 'Inpaint Denoising Strength' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)								in 'Inpaint Respective Field' Slider component
				False,	# bool in 'Enable Mask Upload' Checkbox component
				False,	# bool in 'Invert Mask' Checkbox component
				-64,	# int | float (numeric value between -64 and 64)								in 'Mask Erode or Dilate' Slider component
				False,	# bool in 'Save Metadata to Images' Checkbox component
                "fooocus",	# str in 'Metadata Scheme' Radio component
				self.emptyImage,	# str (filepath or URL to image) in 'Image' Image component
				0,	# int | float (numeric value between 0.0 and 1.0)							in 'Stop At' Slider component
				0,	# int | float (numeric value between 0.0 and 2.0)								in 'Weight' Slider component
				"ImagePrompt",	# str in 'Type' Radio component
				self.emptyImage,	# str (filepath or URL to image)	in 'Image' Image component
				0,	# int | float (numeric value between 0.0 and 1.0)								in 'Stop At' Slider component
				0,	# int | float (numeric value between 0.0 and 2.0)								in 'Weight' Slider component
				"ImagePrompt",	# str in 'Type' Radio component
				self.emptyImage,	# str (filepath or URL to image)	in 'Image' Image component
				0,	# int | float (numeric value between 0.0 and 1.0)								in 'Stop At' Slider component
				0,	# int | float (numeric value between 0.0 and 2.0)								in 'Weight' Slider component
				"ImagePrompt",	# str in 'Type' Radio component
				self.emptyImage,	# str (filepath or URL to image)   in 'Image' Image component
				0,	# int | float (numeric value between 0.0 and 1.0)								in 'Stop At' Slider component
				0,	# int | float (numeric value between 0.0 and 2.0)								in 'Weight' Slider component
				"ImagePrompt",	# str in 'Type' Radio component
                fn_index=self.config.generate+self.config.deltaGenerate
            )

            result = self.getClient().predict(fn_index=self.config.generate+1)

            end_time = timeit.default_timer()
           


            # Generation failure
            if len(result[3]['value'])==0:
                console.printBB(" [b]#"+uid+"[/b] Generation image [error]failed[/error]")
                return {
                    "ajax":True, 
                    "error":True, 
                    "image":False,
                    "uid": uid,
                    "metadata": metadata,
                    "start_time": start_time,
                    "end_time": end_time,
                    "elapsed_time": round((end_time - start_time)*1000),
                    "temp": "", 
                    "name": "",
                    "file_size": "",
                    "result": result
                }

            # Generation success
            if "name" in result[3]['value'][0]:  
                now = datetime.now()
                console.printBB("[hour]"+now.strftime("%H:%M:%S")+"[/hour] [b]#"+uid+"[/b] [ok]Image is generated[/ok]")

                picture=result[3]['value'][0]['name']           
                name=self.outputFolder+"/"+uid+result[3]['value'][0]['name'][-4:]
                shutil.copyfile(picture, name)

                if "action" in metadata:
                    if "compress" in metadata["action"]:
                        if "resize" in metadata["action"]:
                            if "copy" in metadata["action"]:
                                w, h=metadata["action"]["resize"]
                                # dirname = os.path.dirname(sys.argv[0])
                                # filename = utils.pathJoin(dirname, metadata["action"]["copy"])
                                # print("Remove file ? "+filename)
                                # if os.path.exists(filename):  
                                #     print("REMOVE FILE:  "+filename)
                                #    os.remove(filename)
                                utils.resizeAndCompressImage(picture, w, h, metadata["action"]["compress"], metadata["action"]["copy"])

            image={ "ajax": True,
                    "error": False,
                    "image": True,
                    "uid": uid,
                    "metadata": metadata,
                    "start_time": start_time,
                    "end_time": end_time,
                    "elapsed_time": round((end_time - start_time)*1000),
                    "temp": result[3]['value'][0]['name'], 
                    "name": "/"+name,
                    "file_size": os.path.getsize(picture),
                    "result": result      
                }



            return image
        
        except Exception as e:
            if self.config.deltaGenerate<0:
                console.printBB("[warning]sendCreateImage() failed. Trying to find the right gradio API fn_index  (i+"+str(self.config.deltaGenerate)+")[/warning]")
                self.config.deltaGenerate+=1
                return self.sendCreateImage(metadata, uid)
            else:            
                print("sendCreateImage exception")
                print(f"Error: {e}")
                print(" Check the Fooocus console terminal to view more indications")
                traceback.print_exc()  # Print the full traceback
                return {"ajax":True, "error":True}
