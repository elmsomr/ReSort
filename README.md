# ReSort ♻️  
_Intelligent Waste Classification System_

>  Forked from [CankayaUniversity/ceng-407-408-2024-2025-ReSort](https://github.com/CankayaUniversity/ceng-407-408-2024-2025-ReSort)  
>  This fork is currently maintained and developed individually by [github.com/elmsomr](https://github.com/elmsomr).  
>  Ongoing improvements include model optimization, real-time hardware integration, and deployment enhancements for edge devices.

---

##  Project Overview

ReSort is an intelligent recycling system that uses computer vision and sensors to automatically classify waste into four main categories: **metal**, **plastic**, **paper**, and **glass**.  
The system uses **YOLOv11 Nano** for object detection and integrates **stepper motor-driven conveyor mechanics** to automate the sorting process.

It is designed to:
- Improve waste separation efficiency
- Reduce manual labor
- Provide an educational, modular prototype for research

---

##  Key Features

-  Real-time object detection using YOLOv11
-  DeepSORT tracker integration
-  Raspberry Pi 5 + Pi Camera 3 based prototype
-  Stepper motors for bin separation
-  Homing via limit switch & dynamic lateral motion
-  Optional API logging for cloud analytics
-  Diffused LED lighting for consistent vision input

---

##  System Requirements

- Raspberry Pi 5 (4GB)
- Raspberry Pi Camera Module 3
- A4988 stepper drivers
- Stepper motors (NEMA 17)
- Limit switch (for homing functionality)
- External 12V power supply
- Breadboard + jumper wires
- 3D printed parts (frame, mounts, conveyor components)

###  Software Requirements

- Python 3.10+
- Dependencies:
  - `opencv-python`
  - `ultralytics`
  - `gpiozero`
  - `deepsort-realtime`
  - `picamera2`
  - `RPi.GPIO`
  - `numpy`
  - `requests`

---

##  Original Team (2024–2025 Capstone)

| **Name - Surname**          | **Student Number** | **GitHub**                              |
|----------------------------|--------------------|-----------------------------------------|
| Emre Can ERKUL              | 202011007          | [EmreCanErkul](https://github.com/EmreCanErkul)     |
| Fırat Can AĞA               | 202011080          | [Hesoyi](https://github.com/Hesoyi)                 |
| Ahmet Eren BOSTAN           | 202011018          | [ErenBostann](https://github.com/ErenBostann)       |
| Ömer ELMAS                  | 202011209          | [elmsomr](https://github.com/elmsomr)               |
| Fatih Cumhur ÖĞÜTÇÜ         | 202011004          | [Fatihcumhurogutcu](https://github.com/Fatihcumhurogutcu) |

###  Advisor  
- **Dr. Öğr. Üyesi Abdül Kadir Görür – CENG**

---

##  License

This project is shared for educational and research purposes.  
For continued use, modification, or publication, proper attribution to the original team and repository is appreciated.

---

##  Contact

Maintainer: Ömer ELMAS
GitHub: [github.com/elmsomr](https://github.com/elmsomr)
