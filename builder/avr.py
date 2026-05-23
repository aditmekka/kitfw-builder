from pathlib import Path

def find_artifacts(folder):

    folder = Path(folder)

    files = {
        "application": None
    }

    for file in folder.glob("*.hex"):

        name = file.name.lower()

        if "bootloader" in name:
            continue

        files["application"] = file

    return files