# AAE4011-Group-Project
# Guardian AI - Vision-Based Active Hazard Prevention System

**Advanced Driver Assistance System (ADAS) for Vulnerable Road Users**  
**Department of Aeronautical and Aviation Engineering**  
**The Hong Kong Polytechnic University**  
**Group 6: Hung Yan Kin Barney, LAI Ki Uen, LIU Pui Ling**

## Project Description
Guardian AI detects pedestrians, cats, and dogs in vehicle **front-over blind spots** using YOLOv8.  
It employs **empirical video testing** to set pixel-area thresholds: **6000 px (Person)** and **2000 px (Cat/Dog)** at the 3.0 m danger zone.

Key innovations:
- Dynamic Area Dictionary for perspective-aware detection
- Decoupled alerting: Telegram (loud audio siren) + Blynk (visual dashboard)
- Honest latency analysis leading to Raspberry Pi edge computing upgrade

## Setup & Installation

```bash
git clone https://github.com/Barney730/AAE4011-Group-Project-GP6
cd GuardianAI
pip install -r requirements.txt
```
## Usage
```bash
mkdir models
wget https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt -O models/yolov8n.pt
```

## 1. PPT Slide:
* https://connectpolyu-my.sharepoint.com/:p:/g/personal/25134783d_connect_polyu_hk/IQBLkl3NU2hiS4TdyxAONfs6ATRBQ4czjyRWAowTJJOjwfA?e=cbUcyl

## 2. Video (YouTube): 
* Demonstration: https://youtu.be/uMUcCrhCu54?si=-kR9fnlAn9y6GoGl
* GuardianAI: https://youtube.com/shorts/9B2_a3AWMsw?si=3fxfBuCSHNT98Vn1

## Configuration
Edit ```config.py``` to adjust:

* Pixel area thresholds (Person: 6000, Cat/Dog: 2000)
* max_area for dynamic area dictionary
* Alert settings (Telegram Bot Token, Chat ID, Blynk auth)

## Future Work

* Port to Raspberry Pi 5 / NVIDIA Jetson for edge computing (zero latency)
* TensorRT optimization
* Full hardware integration with vehicle camera

## References

* YOLOv8 by Ultralytics
* WHO Road Traffic Injuries Fact Sheet
* IIHS Blind Spot Research
* Hong Kong Transport Department Accident Statistics


---

### 2. `requirements.txt`

```txt
ultralytics
opencv-python
numpy
requests
blynklib
python-telegram-bot
PyYAML
