import os
import re
from collections import defaultdict

# Klasör yollarını belirtin

images_dir = "C:/Users/ASUS/Desktop/eniyidatasetVol2/mixdata/train/images"
labels_dir = "C:/Users/ASUS/Desktop/eniyidatasetVol2/mixdata/train/labels"
log_path = os.path.join(os.path.dirname(images_dir), "temizlik_log.txt")

# Uzantılara göre filtreleme
image_exts = ('.jpg', '.jpeg', '.png')

def normalize_name(filename):
    """img(1).jpg → img, img - kopya.jpg → img"""
    name = os.path.splitext(filename)[0]
    name = re.sub(r'[\s_-]*kopya|\(\d+\)$', '', name, flags=re.IGNORECASE)
    return name.lower()

def clean_duplicates(folder, exts):
    name_map = defaultdict(list)
    for fname in os.listdir(folder):
        if fname.lower().endswith(exts):
            norm = normalize_name(fname)
            name_map[norm].append(fname)

    deleted = []
    for norm_name, files in name_map.items():
        if len(files) > 1:
            # Sadece ilk dosyayı tut, diğerlerini sil
            files_to_delete = files[1:]
            for f in files_to_delete:
                path = os.path.join(folder, f)
                if os.path.exists(path):
                    os.remove(path)
                    deleted.append(path)
    return deleted

with open(log_path, "a", encoding="utf-8") as log_file:
    log_file.write("\n### Çift Dosya Temizliği ###\n\n")

    # Görsellerde tekrar kontrolü
    deleted_imgs = clean_duplicates(images_dir, image_exts)
    for path in deleted_imgs:
        print(f"Silinen kopya görsel: {path}")
        log_file.write(f"Silinen kopya görsel: {path}\n")

    # Etiketlerde tekrar kontrolü
    deleted_labels = clean_duplicates(labels_dir, ('.txt',))
    for path in deleted_labels:
        print(f"Silinen kopya etiket: {path}")
        log_file.write(f"Silinen kopya etiket: {path}\n")
