#Bir dosyadaki fotoğrafları başka klasöre taşıdığımda kendi otomatik txt dosyalarını da başka klasöre taşıyor

import os
import shutil

images_source = "C:/Users/ASUS/Desktop/15kdüzenlenmişdata/mixdata/test/images" 
labels_source = "C:/Users/ASUS/Desktop/15kdüzenlenmişdata/mixdata/test/labels"  

images_target = "C:/Users/ASUS/Desktop/15kdüzenlenmişdata/mixdata/değiştirme/images" 
labels_target = "C:/Users/ASUS/Desktop/15kdüzenlenmişdata/mixdata/değiştirme/labels" 

os.makedirs(labels_target, exist_ok=True)

moved_images = {os.path.splitext(f)[0] for f in os.listdir(images_target) if f.endswith((".jpg", ".png"))}

moved_labels = 0

# test/labels içindeki .txt dosyalarını kontrol et
for label_file in os.listdir(labels_source):
    if label_file.endswith(".txt"):
        label_name = os.path.splitext(label_file)[0] 
        
        if label_name in moved_images:  
            shutil.move(os.path.join(labels_source, label_file), os.path.join(labels_target, label_file))
            moved_labels += 1
            print(f"✅ Taşındı: {label_file}")

print(f"🎯 {moved_labels} etiket dosyası {labels_target} klasörüne taşındı.")