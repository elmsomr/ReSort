import os

labels_dir = "C:/Users/ASUS/Desktop/paper/test/labels"  

deleted_files = 0

for file in os.listdir(labels_dir):
    file_path = os.path.join(labels_dir, file)
    
    if file.endswith(".txt") and os.path.getsize(file_path) == 0:  
        os.remove(file_path)  
        deleted_files += 1
        print(f"Silindi: {file}")

print(f"✅ {deleted_files} boş etiket dosyası silindi.")
