from builder.esp32 import find_artifacts
from builder.manifest import create_manifest

folder = input(
    "ESP32 build folder: "
)

files = find_artifacts(folder)

manifest = create_manifest(
    "Water Level Monitor",
    "1.0.0",
    "esp32",
    files
)

print(manifest)