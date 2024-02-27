import psutil
import cpuinfo
import GPUtil
import timeit
import platform
from src import console
from src import utils


# Get hardware informations about the device (CPU, RAM, GPU)
def getDeviceInfo():
    start_time0 = timeit.default_timer()

    start_time = timeit.default_timer()
    try:
        gpus = GPUtil.getGPUs()
        gpu_info = [{'id': gpu.id, 
                    'uuid': gpu.uuid, 
                    'name': gpu.name, 
                    'serial': gpu.serial, 
                    'temperature': gpu.temperature, 
                    'load': gpu.load, 
                    'memoryTotal': gpu.memoryTotal, 
                    'memoryUtil': gpu.memoryUtil,
                    'memoryUsed': gpu.memoryUsed,
                    'memoryFree': gpu.memoryFree,
                    'display_mode': gpu.display_mode,
                    'display_active': gpu.display_active
                    } 
                    for gpu in gpus]
    except:
        gpu_info = [{
            'id': "", 
            'uuid': "", 
            'name': "", 
            'serial': "", 
            'temperature': "", 
            'load': "", 
            'memoryTotal': 0, 
            'memoryUtil': 0,
            'memoryUsed': 0,
            'memoryFree': 0,
            'display_mode': "",
            'display_active': ""}]
        console.printBB(" [d] GPUtil is ignored in this python version [/d]")

    end_time = timeit.default_timer()
    #print(f"Execution time GPUtil.getGPUs(): {end_time - start_time} seconds")

    try:
        cpu_util = psutil.cpu_freq()
        end_time = timeit.default_timer()
        #print(f"Execution time psutil.cpu_freq(): {end_time - start_time0} seconds")
        
        start_time = timeit.default_timer()
        cpu_name = cpuinfo.get_cpu_info()
        end_time = timeit.default_timer()
        #print(f"Execution time cpuinfo.get_cpu_info(): {end_time - start_time} seconds")
            
        start_time = timeit.default_timer()
        ram_info = psutil.virtual_memory()
        end_time = timeit.default_timer()
        #print(f"Execution time psutil.virtual_memory(): {end_time - start_time} seconds")
                

        start_time = timeit.default_timer()
        hdd_info = psutil.disk_usage('/')
        end_time = timeit.default_timer()
        #print(f"Execution time psutil.disk_usage(): {end_time - start_time} seconds")

        #new object to return 
        device = {
            "detected": True,
            "raw": {
                "cpu_util": cpu_util,
                "cpu_name": cpu_name,
                "ram_info": ram_info,
                "gpus": gpu_info,
                "hdd_info": hdd_info
            },
            "cpu_brand": cpu_name.get("vendor_id_raw"),
            "cpu_name": cpu_name.get("brand_raw"),
            "cpu_freq": cpu_name.get("hz_advertised")[0],
            "cpu_threads": cpu_name.get("count"),
            "cpu_max_freq": cpu_name.get("hz_advertised"),
            "l3_cache_size": cpu_name.get("l3_cache_size"),
            "cpu_arch": cpu_name.get("arch"),
            "ram_installed": ram_info[0],
            "hdd_total": hdd_info.total,
            "hdd_used": hdd_info.used,
            "hdd_free": hdd_info.free,
            "gpus": gpu_info,
            "getDeviceInfoTime": end_time - start_time0,
            "os_name": platform.system(),
            "os_version": platform.release(),
            "os_details": platform.platform(),
            "description": ""
        }
        device["description"] = f"""CPU: {device.get("cpu_name")} - {utils.formatFrequencies(device.get("cpu_freq"))} {device.get("cpu_threads")} threads - {utils.formatBytes(device.get("l3_cache_size"))} L3 cache
        RAM: {utils.formatBytes(round(device.get("ram_installed"), 0))}
        HDD: Total: {utils.formatBytes(device.get("hdd_total"))} Free: {utils.formatBytes(device.get("hdd_free"))}\n"""

        if len(device.get("gpus")) == 0:
            device["description"] = f"No GPU found"
        else:
            gpu=device.get("gpus")[0]
            device["description"] += f"""GPU: {gpu.get("name")} ({gpu.get("memoryTotal")/1024} GB)"""

        device["description"] += f"""\nOS: {device.get("os_name")} {device.get("os_version")}"""
    except:
        console.printBB(" [d] getDeviceInfo() is ignored with your device [/d]")
        device = {
            "detected": False,
            "raw": {
                "cpu_util": "",
                "cpu_name": "",
                "ram_info": "",
                "gpus": gpu_info,
                "hdd_info": ""
            },
            "cpu_brand": "",
            "cpu_name": "",
            "cpu_freq": "",
            "cpu_threads": "",
            "cpu_max_freq": "",
            "l3_cache_size": "",
            "cpu_arch": "",
            "ram_installed": "",
            "hdd_total": "",
            "hdd_used": "",
            "hdd_free": "",
            "gpus": gpu_info,
            "getDeviceInfoTime": 0,
            "os_name": platform.system(),
            "os_version": platform.release(),
            "os_details": platform.platform(),
            "description": "Hardware not detected"
        }

    return device


