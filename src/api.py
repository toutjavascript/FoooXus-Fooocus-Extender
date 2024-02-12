import os
import shutil
import traceback
import timeit
import pprint
from src import utils
from gradio_client import Client


class FooocusApi:
    def __init__(self, base_url, outputFolder="outputs/tmp"):
        self.client=None
        self.outputFolder=outputFolder
        if base_url[0:7] != "http://"[0:7]:
            base_url="http://"+base_url
        self.base_url = base_url.strip()
        self.emptyImage="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABh6FO1AAAAABJRU5ErkJggg=="

    def getClient(self):
        if (self.client==None):
            print("Open API client to Fooocus instance at "+self.base_url+" ...")
            try:
                self.client = Client(self.base_url, serialize=False)
                print("Client opened")
                return self.client
            except Exception as e:
                self.client=None
                print("Client not opened")
                print(f"Error: {e}")
                return None
        else:
            return self.client
    

    # Ping Fooocus instance 
    def pingFooocus(self):
        print("py.pingFooocus() ")
        try:
            client=self.getClient();
            result = client.predict( fn_index=9 )
            return {"ajax":True, "error":False, "ping":True, "fooocusUrl": self.base_url}
        except Exception as e:
            print("pingFooocus exception")
            print(f"Error: {e}")
            return {"ajax":True, "error":True}


    # Get list of all models installed on the Fooocus folder
    def getModels(self):
        try:
            result = self.getClient().predict( fn_index=24 )
            models=[]
            if (result[0]):
                if (result[0]["choices"]):
                    for model in result[0]["choices"]:
                        models.append(model)
            return {"ajax":True, "error":False, "models":models}
        except Exception as e:
            print("getModels exception")
            print(f"Error: {e}")
            return {"ajax":True, "error":True}


    # Get all styles available for Fooocus
    def getStyles(self):
        try:
            result = self.getClient().predict( [], fn_index=19 )
            styles=[]
            if ("choices" in result):
                for style in result["choices"]:
                    styles.append(style[0])
            return {"ajax":True, "error":False, "styles":styles}
        except:
            return {"ajax":True, "error":True}

    # Get all Loras from the loras-directory
    def getLoras(self, dir):
        try:
            loras=utils.getFiles(dir, ".safetensors")
            return {"ajax":True, "error":False, "loras":loras}
        except:
            return {"ajax":True, "error":True}
            

    def initFooocus(self, metadata={}):
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
				fn_index=33
            )
            return {"ajax":True, "error":False, "init":True}
        except Exception as e:
            print("getModels exception")
            print(f"Error: {e}")
            return {"ajax":True, "error":True}



    def sendCreateImage(self, metadata, uid):
        print("  py.sendCreateImage() ")

        try:
            start_time = timeit.default_timer()
            self.initFooocus(metadata)
            print("  waiting for predict() ")

            result = self.getClient().predict( 
                metadata["Prompt"],	        # str in 'parameter_10' Textbox component
                metadata["Negative Prompt"],# str in 'Negative Prompt' Textbox component
                metadata["Styles"],	        # List[str] in 'Selected Styles' Checkboxgroup component
                metadata["Performance"],	# str in 'Performance' Radio component
                '1024×1024',	            # str in 'Aspect Ratios' Radio component
                1,	                        # int | float (numeric value between 1 and 64)	in 'Image Number' Slider component
                metadata["Seed"],	        # str in 'Seed' Textbox component
                metadata["Sharpness"],	    # int | float (numeric value between 0.0 and 30.0)	in 'Image Sharpness' Slider component
                metadata["Guidance Scale"],	# int | float (numeric value between 1.0 and 30.0)	in 'Guidance Scale' Slider component
                metadata["Base Model"], 	# str 	in 'Base Model (SDXL only)' Dropdown component
                metadata["Refiner Model"],	# str 	in 'Refiner (SDXL or SD 1.5)' Dropdown component
                metadata["Refiner Switch"],	# int | float (numeric value between 0.1 and 1.0)	in 'Refiner Switch At' Slider component
                metadata["Lora 1"],	        # str 	in 'LoRA 1' Dropdown component
                metadata["Weight Lora 1"],	# int | float (numeric value between -2 and 2)		in 'Weight' Slider component
                metadata["Lora 2"],	        # str 	in 'LoRA 2' Dropdown component
                metadata["Weight Lora 2"],	# int | float (numeric value between -2 and 2)		in 'Weight' Slider component
                metadata["Lora 3"],	        # str 	in 'LoRA 3' Dropdown component
                metadata["Weight Lora 3"],	# int | float (numeric value between -2 and 2)		in 'Weight' Slider component
                metadata["Lora 4"],	        # str 	in 'LoRA 4' Dropdown component
                metadata["Weight Lora 4"],	# int | float (numeric value between -2 and 2)		in 'Weight' Slider component
                metadata["Lora 5"],	        # str 	in 'LoRA 5' Dropdown component
                metadata["Weight Lora 5"],	# int | float (numeric value between -2 and 2)		in 'Weight' Slider component
                False,	# bool in 'Input Image' Checkbox component
                "",	# str in 'parameter_85' Textbox component
                "Disabled",	# str in 'Upscale or Variation:' Radio component
                self.emptyImage,	# str (filepath or URL to image)				in 'Drag above image to here' Image component
                ["Left"],	# List[str] in 'Outpaint Direction' Checkboxgroup component
                self.emptyImage,	# str (filepath or URL to image)				in 'Drag inpaint or outpaint image to here' Image component
                "",	# str in 'Inpaint Additional Prompt' Textbox component
                self.emptyImage,	# str (filepath or URL to image)				in 'Mask Upload' Image component
                self.emptyImage,	# str (filepath or URL to image)				in 'Image' Image component
                0,	# int | float (numeric value between 0.0 and 1.0)				in 'Stop At' Slider component
                0,	# int | float (numeric value between 0.0 and 2.0)			    in 'Weight' Slider component
                "ImagePrompt",	# str in 'Type' Radio component
                self.emptyImage,	# str (filepath or URL to image)				in 'Image' Image component
                0,	# int | float (numeric value between 0.0 and 1.0)				in 'Stop At' Slider component
                0,	# int | float (numeric value between 0.0 and 2.0)				in 'Weight' Slider component
                "ImagePrompt",	# str in 'Type' Radio component
                self.emptyImage,	# str (filepath or URL to image)				in 'Image' Image component
                0,	# int | float (numeric value between 0.0 and 1.0)				in 'Stop At' Slider component
                0,	# int | float (numeric value between 0.0 and 2.0)				in 'Weight' Slider component
                "ImagePrompt",	# str in 'Type' Radio component
                self.emptyImage,	# str (filepath or URL to image)				in 'Image' Image component
                0,	# int | float (numeric value between 0.0 and 1.0)				in 'Stop At' Slider component
                0,	# int | float (numeric value between 0.0 and 2.0)				in 'Weight' Slider component
                "ImagePrompt",	# str in 'Type' Radio component
                fn_index=34
            )

            print("type(result)")
            print(type(result))
            pprint.pprint(result)

            end_time = timeit.default_timer()

            

            # Generation failure
            if len(result[3]['value'])==0:
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
                picture=result[3]['value'][0]['name']           
                name=self.outputFolder+"/"+uid+result[3]['value'][0]['name'][-4:]
                shutil.copy(picture, name)

                if "action" in metadata:
                    if "compress" in metadata["action"]:
                        if "resize" in metadata["action"]:
                            if "copy" in metadata["action"]:
                               w, h=metadata["action"]["resize"]
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
            print("sendCreateImage exception")
            print(f"Error: {e}")
            traceback.print_exc()  # Print the full traceback
            return {"ajax":True, "error":True}
