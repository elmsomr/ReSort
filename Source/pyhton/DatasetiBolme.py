#Dataseti train valid test diye istediğin orana göre bölüyor

import os
import random
import shutil

source_folder = "C:/Users/ASUS/Desktop/ANN PROJ/Yolo Truck.v1i.yolov11/train/images"   
output_folder = "C:/Users/ASUS/Desktop/ANN PROJ/Yolo Truck.v1i.yolov11/train/split"    

train_ratio = 0.8
valid_ratio = 0.1
test_ratio = 0.1

assert abs(train_ratio + valid_ratio + test_ratio - 1.0) < 1e-6, "Oranlar toplamı 1 olmalı!"

all_images = [f for f in os.listdir(source_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
random.shuffle(all_images)  

total = len(all_images)
train_count = int(total * train_ratio)
valid_count = int(total * valid_ratio)

train_images = all_images[:train_count]
valid_images = all_images[train_count:train_count + valid_count]
test_images = all_images[train_count + valid_count:]


for split in ['train', 'valid', 'test']:
    os.makedirs(os.path.join(output_folder, split, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_folder, split, 'labels'), exist_ok=True)


def move_files(file_list, split_name):
    for filename in file_list:
        src_img = os.path.join(source_folder, filename)
        dst_img = os.path.join(output_folder, split_name, 'images', filename)
        shutil.move(src_img, dst_img)

        label_name = os.path.splitext(filename)[0] + '.txt'
        src_label = os.path.join(source_folder.replace('images', 'labels'), label_name)
        dst_label = os.path.join(output_folder, split_name, 'labels', label_name)
        if os.path.exists(src_label):
            shutil.move(src_label, dst_label)

move_files(train_images, 'train')
move_files(valid_images, 'valid')
move_files(test_images, 'test')

print(f"Bölme tamamlandı: {len(train_images)} train, {len(valid_images)} valid, {len(test_images)} test dosyası oluşturuldu.")
