#Etiketi yoksa fotoğrafı sil

import os

labels_dir = "C:/Users/ASUS/Desktop/Vehicle detection and Management.v1i.yolov11/valid/labels"   
images_dir = "C:/Users/ASUS/Desktop/Vehicle detection and Management.v1i.yolov11/valid/images"   


label_files = {os.path.splitext(f)[0] for f in os.listdir(labels_dir) if f.endswith(".txt")}

deleted_files = 0

for image_file in os.listdir(images_dir):
    if image_file.endswith((".jpg", ".png")):  
        image_name = os.path.splitext(image_file)[0]  
        
        if image_name not in label_files: 
            os.remove(os.path.join(images_dir, image_file)) 
            deleted_files += 1
            print(f"Silindi: {image_file}")

print(f"✅ {deleted_files} fotoğraf silindi.")
