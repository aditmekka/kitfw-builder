# In manifest.py

# Flash offset mappings for different ESP chips
ESP_OFFSETS = {
    # Classic ESP32
    "esp32": {
        "bootloader": "0x1000",
        "partitions": "0x8000",
        "application": "0x10000"
    },
    # ESP32-S2
    "esp32s2": {
        "bootloader": "0x1000",
        "partitions": "0x8000",
        "application": "0x10000"
    },
    # ESP32-S3, C3, C6, H2 (newer chips use 0x0 for bootloader)
    "esp32s3": {
        "bootloader": "0x0",
        "partitions": "0x8000",
        "application": "0x10000"
    },
    "esp32c3": {
        "bootloader": "0x0",
        "partitions": "0x8000",
        "application": "0x10000"
    },
    "esp32c6": {
        "bootloader": "0x0",
        "partitions": "0x8000",
        "application": "0x10000"
    },
    "esp32h2": {
        "bootloader": "0x0",
        "partitions": "0x8000",
        "application": "0x10000"
    },
    # ESP8266 (special case)
    "esp8266": {
        "bootloader": None,  # No separate bootloader
        "partitions": None,   # No partition table
        "application": "0x0"
    }
}

def create_manifest(name, version, target, files, avr_config=None, esp_config=None):
    manifest = {
        "format_version": 1,
        "name": name,
        "version": version,
        "target": target,
        "flash": []
    }
    
    if target == "espressif":
        chip = esp_config.get("chip", "esp32")
        offsets = ESP_OFFSETS.get(chip, ESP_OFFSETS["esp32"])
        
        # Store ESP config in manifest
        manifest["esp"] = esp_config
        
        if files["merged"]:
            # Merged firmware - single file contains everything
            manifest["flash"].append({
                "address": "0x0",
                "file": files["merged"].name
            })
        else:
            # Fragmented firmware - separate files
            if files["bootloader"] and offsets["bootloader"]:
                manifest["flash"].append({
                    "address": offsets["bootloader"],
                    "file": files["bootloader"].name
                })
            
            if files["partitions"] and offsets["partitions"]:
                manifest["flash"].append({
                    "address": offsets["partitions"],
                    "file": files["partitions"].name
                })
            
            if files["application"]:
                manifest["flash"].append({
                    "address": offsets["application"],
                    "file": files["application"].name
                })
    
    elif target == "avr":
        if avr_config:
            manifest["avr"] = avr_config
        else:
            manifest["avr"] = {
                "mcu": "atmega328p",
                "programmer": "arduino",
                "baud_rates": [115200, 57600]
            }
        
        manifest["flash"].append({
            "file": files["application"].name
        })
    
    return manifest