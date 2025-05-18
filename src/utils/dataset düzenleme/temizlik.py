import os

# Klasör yollarını belirtin
images_dir = "C:/Users/ASUS/Desktop/eniyidatasetVol2/mixdata/test/images"
labels_dir = "C:/Users/ASUS/Desktop/eniyidatasetVol2/mixdata/test/labels"
log_path = os.path.join(os.path.dirname(images_dir), "temizlik_log.txt")

# Etiket ve görsel isimlerini (uzantısız) topla
image_files = {os.path.splitext(f)[0] for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))}
label_files = {os.path.splitext(f)[0] for f in os.listdir(labels_dir) if f.endswith('.txt')}

with open(log_path, "w", encoding="utf-8") as log_file:
    log_file.write("### Temizlik Logu ###\n\n")

    # Eşleşmeyen görselleri sil
    for img_name in image_files - label_files:
        for ext in ('.jpg', '.jpeg', '.png'):
            img_path = os.path.join(images_dir, img_name + ext)
            if os.path.exists(img_path):
                os.remove(img_path)
                msg = f"Silinen görsel: {img_path}"
                print(msg)
                log_file.write(msg + "\n")

    # Eşleşmeyen etiketleri sil
    for label_name in label_files - image_files:
        label_path = os.path.join(labels_dir, label_name + '.txt')
        if os.path.exists(label_path):
            os.remove(label_path)
            msg = f"Silinen etiket: {label_path}"
            print(msg)
            log_file.write(msg + "\n")
