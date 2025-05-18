#Polygon etiketlerini silme

import os

main_folder = "C:/Users/ASUS/Desktop/roboflowclasscıkardımdataset"

subfolders = ["test", "train", "valid"]

deleted_files = 0 

for subfolder in subfolders:
    labels_path = os.path.join(main_folder, subfolder, "labels")

    if os.path.exists(labels_path) and os.path.isdir(labels_path):
        for file in os.listdir(labels_path):
            file_path = os.path.join(labels_path, file)
            
            if not file.endswith(".txt") or not os.path.isfile(file_path):
                continue
            
            if os.stat(file_path).st_size == 0:
                os.remove(file_path)
                deleted_files += 1
                print(f"Silindi (Boş Dosya): {file}")
                continue
            
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            contains_polygon = any(len(line.strip().split()) > 5 for line in lines)

            if contains_polygon:
                os.remove(file_path)  
                deleted_files += 1
                print(f"Silindi (Polygon Etiketi): {file}")

print(f"✅ {deleted_files} dosya silindi.")