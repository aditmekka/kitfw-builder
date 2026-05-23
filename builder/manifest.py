def create_manifest(
        name,
        version,
        target,
        files):

    manifest = {

        "format_version": 1,

        "name": name,

        "version": version,

        "target": target,

        "flash": []
    }

    if target == "esp32":

        if files["merged"]:

            manifest["flash"].append({

                "address": "0x0",

                "file":
                files["merged"].name
            })

        else:

            manifest["flash"].append({

                "address": "0x1000",

                "file":
                files["bootloader"].name
            })

            manifest["flash"].append({

                "address": "0x8000",

                "file":
                files["partitions"].name
            })

            manifest["flash"].append({

                "address": "0x10000",

                "file":
                files["application"].name
            })

    elif target == "esp8266":

        manifest["flash"].append({

            "address": "0x0",

            "file":
            files["application"].name
        })

    elif target == "avr":

        manifest["flash"].append({

            "file":
            files["application"].name
        })

    return manifest