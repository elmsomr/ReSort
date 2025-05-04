#Hangi classtan kaç adet instance olduğunu gösterir

import os
from collections import defaultdict

labels_dir = "C:/Users/ASUS/Desktop/eniyidataset/mixdata/train/labels"  

label_counts = defaultdict(int)

for file in os.listdir(labels_dir):
    file_path = os.path.join(labels_dir, file)
    
    if file.endswith(".txt"):  
        with open(file_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 1:  
                label = parts[0]  
                label_counts[label] += 1  

print("📊 Etiket Dağılımı:")
for label, count in sorted(label_counts.items(), key=lambda x: int(x[0])):  
    print(f"Etiket {label}: {count} adet")

print("✅ Etiket sayımı tamamlandı.")
