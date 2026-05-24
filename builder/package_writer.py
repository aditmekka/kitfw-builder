import json
import zipfile

def write_package(
        output_file,
        manifest,
        files):

    available_files = {}

    for path in files.values():

        if path:

            available_files[
                path.name
            ] = path

    with zipfile.ZipFile(
            output_file,
            "w",
            zipfile.ZIP_DEFLATED
    ) as z:

        z.writestr(
            "manifest.json",

            json.dumps(
                manifest,
                indent=4
            )
        )

        for entry in manifest["flash"]:

            filename = entry["file"]

            path = available_files[
                filename
            ]

            z.write(
                path,
                filename
            ) 