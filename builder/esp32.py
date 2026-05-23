from pathlib import Path

def find_artifacts(folder):

    folder = Path(folder)

    files = {
        "merged": None,
        "bootloader": None,
        "partitions": None,
        "application": None
    }

    for file in folder.glob("*.bin"):

        name = file.name.lower()

        if "merged" in name:

            files["merged"] = file

        elif "bootloader" in name:

            files["bootloader"] = file

        elif "partitions" in name:

            files["partitions"] = file

        else:

            files["application"] = file

    return files