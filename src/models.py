class DeviceInfo:
    def __init__(self, cpu_name, cpu_freq, ram_info, gpu_info, hdd_info):
        self.cpu_name = cpu_name
        self.cpu_freq = cpu_freq
        self.ram_info = ram_info
        self.gpu_info = gpu_info
        self.hdd_info = hdd_info

    def __str__(self):
        return f"CPU: {self.cpu_name}\nCPU Frequency: {self.cpu_freq}\nRAM: {self.ram_info}\nGPU: {self.gpu_info}\nHDD: {self.hdd_info}"

    def __repr__(self):
        return f"CPU: {self.cpu_name}\nCPU Frequency: {self.cpu_freq}\nRAM: {self.ram_info}\nGPU: {self.gpu_info}\nHDD: {self.hdd_info}"

    def getDevice(self):
        cpu_name = "Intel(R) Core(TM) i7-7700HQ CPU @ 2.80GHz"
        cpu_freq = "2.8 GHz"
        ram_info = "16 GB"
        gpu_info = "NVIDIA GeForce GTX 1050 Ti"
        hdd_info = "1 TB"
        return DeviceInfo(cpu_name, cpu_freq, ram_info, gpu_info, hdd_info)

class Metadata: 
    def __init__(self, prompt, negativePrompt, selectedStyles, performance, aspectRatios, imageNumber, seed, imageSharpness, guidanceScale, baseModel, refiner, refinerSwitchAt, lora1, weight1, lora2, weight2, lora3, weight3, lora4, weight4, lora5, weight5):
        self.prompt = prompt
        self.negativePrompt = negativePrompt
        self.selectedStyles = selectedStyles
        self.performance = performance
        self.aspectRatios = aspectRatios
        self.imageNumber = imageNumber
        self.seed = seed
        self.imageSharpness = imageSharpness
        self.guidanceScale = guidanceScale
        self.baseModel = baseModel
        self.refiner = refiner
        self.refinerSwitchAt = refinerSwitchAt
        self.lora1 = lora1
        self.weight1 = weight1
        self.lora2 = lora2
        self.weight2 = weight2
        self.lora3 = lora3
        self.weight3 = weight3
        self.lora4 = lora4
        self.weight4 = weight4
        self.lora5 = lora5
        self.weight5 = weight5
        

class Image:
    def __init__(self, metadata, uid, path, start_time, end_time, elapsed_time):
        self.metadata = metadata
        self.uid = uid
        self.path = path
        self.start_time = start_time
        self.end_time = end_time
        self.elapsed_time = elapsed_time

