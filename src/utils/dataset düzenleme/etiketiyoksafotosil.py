#Etiket dosyası yoksa fotoğrafı silme

import os

labels_dir = "C:/Users/ASUS\Desktop/Atik Ayristirma.v1i.yolov11/train/labels"  
images_dir = "C:/Users/ASUS\Desktop/Atik Ayristirma.v1i.yolov11/train/images"  

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


