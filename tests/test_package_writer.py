from builder.avr import find_artifacts
from builder.manifest import create_manifest
from builder.validators import (validate_manifest, validate_files)
from builder.package_writer import write_package

folder = input(
    "AVR build folder: "
)

files = find_artifacts(folder)

print(files)

manifest = create_manifest(
    "Arduino Test",
    "0.1.0",
    "avr",
    files
)

print(manifest)

validate_manifest(manifest)
validate_files(manifest, files)

write_package("test_output.kitfw", manifest, files)
