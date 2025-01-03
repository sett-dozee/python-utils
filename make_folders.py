import os

total_folders = 1000
for i in range(1000, 1000 + total_folders):
    folder_name = f"R000{i}"
    os.makedirs("./folders/" + folder_name)
    folder_name = f"F000{i}"
    os.makedirs("./folders/" + folder_name)
