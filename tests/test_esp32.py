from builder.esp32 import find_artifacts

folder = input(
    "ESP32 build folder: "
)

files = find_artifacts(folder)

print()

for key, value in files.items():

    print(
        f"{key}: {value}"
    )