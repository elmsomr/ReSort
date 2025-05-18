#Fotoğraf karşılığı yoksa etiketleri silme 

import os

labels_dir = "C:/Users/ASUS/Desktop/Vehicle detection and Management.v1i.yolov11/train/labels"   
images_dir = "C:/Users/ASUS/Desktop/Vehicle detection and Management.v1i.yolov11/train/images"   

image_files = {os.path.splitext(f)[0] for f in os.listdir(images_dir) if f.endswith((".jpg", ".png"))}

deleted_files = 0

for label_file in os.listdir(labels_dir):
    if label_file.endswith(".txt"):  
        label_name = os.path.splitext(label_file)[0]  
        
        if label_name not in image_files:  
            os.remove(os.path.join(labels_dir, label_file))  
            deleted_files += 1
            print(f"Silindi: {label_file}")

print(f"✅ {deleted_files} fazla etiket dosyası silindi.")







