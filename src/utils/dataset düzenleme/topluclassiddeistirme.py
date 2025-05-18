import os


class_mapping = {0: 3}  # Yeni class sırası

# Daha fazla eşleştirme ekleyebilirsin: {0: 3, 1: 0, 2: 1} 

labels_dir = "C:/Users/ASUS/Desktop/JustplasticBootle/valid/labels"

for filename in os.listdir(labels_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(labels_dir, filename)
        
        with open(file_path, "r") as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            old_class_id = int(parts[0])
            new_class_id = class_mapping[old_class_id]
            new_line = f"{new_class_id} " + " ".join(parts[1:]) + "\n"
            new_lines.append(new_line)
        
        with open(file_path, "w") as f:
            f.writelines(new_lines)

print("Class ID'leri başarıyla güncellendi!")
