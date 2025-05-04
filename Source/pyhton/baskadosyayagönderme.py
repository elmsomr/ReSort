#Seçtiğin class id'sine sahip olan classı başka dosyaya gönderiyor

import os
import shutil

labels_src = r= "C:/Users/ASUS/Desktop/mixfotolar/Somewhat-Final.v1i.yolov11/train/labels"
images_src = r= "C:/Users/ASUS/Desktop/mixfotolar/Somewhat-Final.v1i.yolov11/train/images"

dest_dir = r= "C:/Users/ASUS/Desktop/eklemevol2/plastic/images"

os.makedirs(dest_dir, exist_ok=True)

possible_exts = [".jpg", ".jpeg", ".png", ".bmp"]

for filename in os.listdir(labels_src):
    if filename.endswith(".txt"):
        label_path = os.path.join(labels_src, filename)
        
        with open(label_path, "r") as file:
            lines = file.readlines()
        
        move_flag = any(line.strip().split() and line.strip().split()[0] == "4" for line in lines)
        
        if move_flag:
            print("Taşınıyor (etiket):", label_path)
            shutil.move(label_path, os.path.join(dest_dir, filename))
            
            base_name = os.path.splitext(filename)[0]
            image_found = False
            for ext in possible_exts:
                image_file = base_name + ext
                image_path = os.path.join(images_src, image_file)
                if os.path.exists(image_path):
                    print("Taşınıyor (resim):", image_path)
                    shutil.move(image_path, os.path.join(dest_dir, image_file))
                    image_found = True
                    break  
            if not image_found:
                print("Resim dosyası bulunamadı:", base_name)
