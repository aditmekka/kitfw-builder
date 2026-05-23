def validate_manifest(manifest):

    if not manifest["name"]:
        raise Exception(
            "Package name is empty"
        )

    if not manifest["version"]:
        raise Exception(
            "Version is empty"
        )

    if not manifest["target"]:
        raise Exception(
            "Target missing"
        )

    if len(manifest["flash"]) == 0:
        raise Exception(
            "No flash entries"
        )
    
def validate_files(
        manifest,
        files):

    available_files = {}

    for path in files.values():

        if path:

            available_files[
                path.name
            ] = path

    for entry in manifest["flash"]:

        filename = entry["file"]

        if filename not in available_files:

            raise Exception(
                f"Missing file: {filename}"
            )