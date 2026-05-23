from pathlib import Path

def find_artifacts(folder):

    folder = Path(folder)

    files = {
        "application": None
    }

    for file in folder.glob("*.bin"):

        name = file.name.lower()

        if name.endswith("ino.bin"):

            files["application"] = file

    return files