## Datasets Used

For the training and evaluation of our object detection model, we used three separate datasets hosted on Roboflow. These datasets consist of annotated images categorized primarily by vehicle or waste types, and are tailored for real-time detection applications. Each dataset was carefully preprocessed and augmented using Roboflow's integrated tools.

### Dataset Links

- [Resort Dataset 1](https://app.roboflow.com/resort)  
  Contains initial image samples with bounding box annotations for key object categories. Used as the base dataset for training.

- [Resort Dataset 2](https://app.roboflow.com/resort2)  
  Includes additional image samples with improved diversity and labeling accuracy. Helped improve model generalization.

- [Resort Dataset 3](https://app.roboflow.com/resort3)  
  Final dataset version containing merged and cleaned annotations. Used for fine-tuning and validation stages.

Each dataset was exported in YOLO format and integrated seamlessly into our training pipeline.

