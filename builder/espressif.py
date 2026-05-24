from pathlib import Path

def find_artifacts(folder):
    """
    Generic ESP artifact finder.
    Works for all ESP chips (ESP32, S3, C3, C6, H2, 8266)
    PRIORITIZES .bin FILES OVER .elf FILES
    """
    folder = Path(folder)
    
    files = {
        "merged": None,
        "bootloader": None,
        "partitions": None,
        "application": None
    }
    
    for file in folder.glob("*"):
        name = file.name.lower()
        
        # Merged firmware
        if ".merged.bin" in name or "merged" in name:
            if file.suffix == ".bin":
                files["merged"] = file
                return files
        
        # Bootloader 
        if "bootloader" in name and file.suffix == ".bin":
            files["bootloader"] = file
        
        # Partition table
        elif ("partition" in name or "partitions" in name) and file.suffix == ".bin":
            files["partitions"] = file
        
        # Application firmware
        elif file.suffix == ".bin" and not files["application"]:
            if "bootloader" not in name and "partition" not in name:
                files["application"] = file
    
    # Second pass: If no .bin files found, fall back to .elf
    if not any([files["merged"], files["bootloader"], files["application"]]):
        for file in folder.glob("*.elf"):
            name = file.name.lower()
            if "bootloader" not in name:
                files["application"] = file
                break
    
    # For ESP8266 style builds (single bin file)
    if not files["merged"] and not files["bootloader"] and files["application"]:
        files["merged"] = files["application"]
        files["application"] = None
    
    return files