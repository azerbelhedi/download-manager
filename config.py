# Base path:
base_path = "/home/azer/Downloads/temp_test"

# Source path:
# New files in this path will be automatically scanned and rearanged/relocated to the target folders
source_path = f"{base_path}/"

# Targert folders
# keywords_file will be used only for .pdf files
target_folders = [
    {
        "path": f"{base_path}/uni/math/",
        "keywords": f"{base_path}/meta/math.txt",
        "row_data": f"{base_path}/meta/math.pdf",
    },

    {
        "path": f"{base_path}/uni/thermo/",
        "keywords": f"{base_path}/meta/thermo.txt",
        "row_data": f"{base_path}/meta/thermo.pdf",
    },

    {
        "path": f"{base_path}/uni/dsal/",
        "keywords": f"{base_path}/meta/dsal.txt",
        "row_data": f"{base_path}/meta/dsal.pdf",
    },
]
archive_target_folder = f"{base_path}/archives/"
pictures_target_folder = f"{base_path}/pictures/"

# Classification threshold
classification_threshold = 0.00005