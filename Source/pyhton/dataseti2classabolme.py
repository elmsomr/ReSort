#2 tane classa ayırmaya çalıştığımda 1 tanesini sabit bırakıyor geri kalanların hepsini 3 olarak etiketliyor yani plastik olarak

import os

labels_dir = "C:/Users/ASUS/Desktop/birlestirireleceksetler/Packaged Food Detection.v1i.yolov11/valid/labels"  

target_label = 3  # Yeni etiket
keep_label = 2    # Korunacak etiket

modified_files = 0

for file in os.listdir(labels_dir):
    if file.endswith(".txt"):  
        file_path = os.path.join(labels_dir, file)

        with open(file_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5: 
                label = int(parts[0])
                if label != keep_label:  # 2 değilse, 3'e çevir
                    label = target_label
                new_lines.append(f"{label} " + " ".join(parts[1:]) + "\n")

        # Dosyayı güncelle
        with open(file_path, "w") as f:
            f.writelines(new_lines)

        modified_files += 1

print(f"✅ {modified_files} dosya güncellendi.")
