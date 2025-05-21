# Dataset Public Link

## https://hub.ultralytics.com/datasets/mK1NOunxolfnf2UnTYfS

## 📁 Dataset

You can access the custom waste classification dataset used in this project via Ultralytics HUB:

🔗 [Click here to view and download the dataset (HiRes) on Ultralytics HUB](https://hub.ultralytics.com/datasets/MocSE0tV7uHhWH9jGeWw)

🔗 [Click here to view and download the dataset (PlasticBottle) on Ultralytics HUB](https://hub.ultralytics.com/datasets/m67zZ5InwqyGJ7H4jURC)

This dataset contains:
- 4 waste categories: Plastic, Glass, Paper, Metal
- Images and YOLO-format labels via Label Studio
- Divided into training and validation sets

💡 To use this dataset in your own training:
```bash
yolo train model=yolov11n.pt data=https://hub.ultralytics.com/datasets/MocSE0tV7uHhWH9jGeWw.yaml
yolo train model=yolov11n.pt data=https://hub.ultralytics.com/datasets/m67zZ5InwqyGJ7H4jURC.yaml
