## Dataset Preparation

In our project, we created a custom dataset by combining and filtering images from three publicly available, pre-labeled datasets on Roboflow. The original datasets contained a wide range of waste categories. However, we selected and retained only the relevant classes for our classification task: **metal**, **paper**, **glass**, and **plastic**.

The filtered and merged datasets are as follows:

- [Resort Dataset 1](https://app.roboflow.com/resort)
- [Resort Dataset 2](https://app.roboflow.com/resort2)
- [Resort Dataset 3](https://app.roboflow.com/resort3)

After selecting only the required classes, we combined all annotated images into a single dataset. This final dataset was then used for training our object detection model. All data was exported in YOLO format for compatibility with our training pipeline.
