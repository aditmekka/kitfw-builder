from builder.esp8266 import find_artifacts
from builder.manifest import create_manifest
from builder.validators import (validate_manifest, validate_files)

folder = input(
    "ESP8266 build folder: "
)

files = find_artifacts(folder)

manifest = create_manifest(
    "NodeMCU Test",
    "0.1.0",
    "esp8266",
    files
)

print(manifest)

validate_manifest(manifest)
validate_files(manifest, files)