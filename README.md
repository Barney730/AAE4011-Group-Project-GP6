# AAE4011-Group-Project
# Guardian AI - Vision-Based Active Hazard Prevention System

**Vision-Based ADAS for Vulnerable Road Users (Pedestrians, Cats, Dogs)**  
**Department of Aeronautical and Aviation Engineering**  
**The Hong Kong Polytechnic University**  
**Group 6: Hung Yan Kin Barney, LAI Ki Uen, LIU Pui Ling**

## Overview
Guardian AI is an intelligent driver assistance system that detects vulnerable road users in vehicle blind spots using YOLOv8. It uses **empirical pixel-area thresholding** (6000 px for humans, 2000 px for cats/dogs) derived from real video testing to trigger proactive alerts via Telegram and Blynk.

### Key Features
- Real-time YOLOv8 object detection (COCO pre-trained weights)
- Empirical dynamic area dictionary for perspective-aware detection
- Dual alerting system: Telegram (audio siren) + Blynk (visual dashboard)
- Optimized thresholds: **6000 px (Person)** | **2000 px (Cat/Dog)**

## Project Report
Full academic report: [`docs/Project_Report.pdf`](docs/Project_Report.pdf)

## Setup & Installation

```bash
git clone https://github.com/Barney730/AAE4011-Group-Project-GP6
cd GuardianAI
pip install -r requirements.txt
```
## Usage
```bash
python main.py --video test_videos/test1.mp4
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
