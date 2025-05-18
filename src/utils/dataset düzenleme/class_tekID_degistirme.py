#Tüm txt yi kontrol et hepsini aynı etikete dönüştür
import os

labels_dir = "C:/Users/ASUS/Desktop/sig2/test/labels"  

modified_files = 0

for file in os.listdir(labels_dir):
    file_path = os.path.join(labels_dir, file)
    
    if file.endswith(".txt"):  
        with open(file_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5:  
                parts[0] = "2"  # Etiket ID'sini 3 olarak değiştir
                new_lines.append(" ".join(parts) + "\n")

        with open(file_path, "w") as f:
            f.writelines(new_lines)

        modified_files += 1

print(f"✅ {modified_files} dosya güncellendi ve tüm etiketler 2'e çevrildi.")
