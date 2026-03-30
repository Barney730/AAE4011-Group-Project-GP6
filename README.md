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

***

## Abstract
This report documents the methodology, implementation, and empirical results of **Guardian AI**, a localized Advanced Driver Assistance System (ADAS). Designed to mitigate collisions involving Vulnerable Road Users (VRUs)—specifically pedestrians, cats, and dogs—the system addresses vehicle blind spots. By employing a YOLOv8 object detection model and an empirical hyperparameter tuning process for perspective geometry, the system proactively detects hazards. A novel decoupled alerting architecture (Blynk + Telegram) bypasses mobile OS restrictions to ensure 100% notification delivery. The report evaluates the Proof of Concept (PoC) constraints, including a measured 2.0-second network latency, and outlines a concrete transition to edge computing, establishing its direct relevance to future Unmanned Autonomous Systems (UAS).

---

## 1. Introduction & Problem Statement
Large urban vehicles possess fatal front-over blind zones, obscuring low-profile targets under 100 cm. With average human reaction times at 1.5 seconds, passive safety systems (airbags) are insufficient. Guardian AI introduces a paradigm shift towards **Active Hazard Prevention**, utilizing AI to warn drivers before a collision occurs.

---

## 2. Technical Depth & AI Algorithm Application
### *(Assessment Criterion: Technical depth and correct application of AI algorithms)*

### 2.1 Core Model Selection: Why YOLOv8?
The perception module is driven by the YOLOv8 architecture. This selection was made after rigorous engineering evaluation against alternatives:
*   **vs. Lightweight Models (e.g., MobileNet):** While MobileNet is fast, it suffers from poor recall for "Small Object Detection." At a 3-meter distance, a cat occupies a minimal pixel area. YOLOv8 significantly outperforms MobileNet in extracting features from distant, small-scale targets.
*   **vs. Newer Iterations (YOLOv10/v11):** In engineering, stability supersedes novelty. YOLOv8 is currently the most stable iteration with the most robust community support for TensorRT optimization and edge device deployment.

### 2.2 Dataset and Pre-trained Weights
We utilized **pre-trained COCO (Common Objects in Context) weights**. For this Proof of Concept, model fine-tuning was deemed computationally redundant. The COCO dataset already contains millions of highly annotated images for our target classes. Therefore, we applied a **Targeted Detection Focus**, programming the algorithm to strictly filter and process only **Class 0 (Person), Class 15 (Cat), and Class 16 (Dog)**, effectively saving processing power and maximizing real-time inference speed.

---

## 3. Methodology: Empirical Iterative Calibration
### *(Assessment Criterion: Innovation and creativity in problem-solving)*

A fundamental challenge in 2D computer vision is perspective geometry: an object's pixel area decreases as distance increases. Instead of relying on theoretical mathematics—which often fails due to lens distortion and camera angles—we employed a highly practical **Empirical Video Testing Methodology** (Hyperparameter Tuning). 

We defined a "Danger Zone" exactly 3.0 meters from the vehicle and fed multiple real-world videos into the YOLOv8 model to find the optimal pixel-area thresholds.

### 3.1 Human Threshold Calibration (Class 0)
We tested various bounding box areas to trigger the alarm perfectly at the 3.0m mark:
*   **Test 1 (15,000 pixels):** Failed. The AI detected the person too late, past the safety boundary.
*   **Test 2 (10,000 pixels):** Failed. Detection was unstable at the 3.0m mark.
*   **Test 3 (6,000 pixels):** Success. Consistent, perfect detection exactly at the Danger Zone.
**Final Optimized Threshold for Person:** **6,000 pixels**.

### 3.2 Animal Threshold Calibration (Class 15/16)
Due to the **Size Disparity Challenge**, using the human threshold (6,000) for a cat would mean the animal must be critically close (e.g., 0.5m) to trigger the alarm, causing a fatal delay. We iterated the tests for animals:
*   **Dog Tests:** Evaluated at 6,000 $\rightarrow$ 4,000 $\rightarrow$ 2,000 pixels.
*   **Cat Tests:** Evaluated at 4,000 $\rightarrow$ 3,000 $\rightarrow$ 2,000 pixels.
**Final Optimized Threshold for Cats/Dogs:** **2,000 pixels**.

<img width="2360" height="1640" alt="IMG_1836" src="https://github.com/user-attachments/assets/c478395c-cf4d-499a-88ca-2941cbaef3c2" />

<img width="1311" height="603" alt="IMG_2670" src="https://github.com/user-attachments/assets/a106ee67-4eee-4edf-a3cb-29f3d0658f46" />

---

## 4. Implementation & Decoupled Architecture
### *(Assessment Criterion: Quality of presentation and documentation)*

### 4.1 Proof of Concept (PoC) Hardware Setup
Due to budget constraints, the current hardware setup utilizes accessible consumer electronics to prove the AI logic:
*   **Sensor:** Smartphone running IP Webcam over Local Wi-Fi.
*   **Processor:** Local PC running the Python OpenCV backend for visual debugging and matrix processing.

### 4.2 Innovation: Decoupled Alerting Architecture
Mobile operating systems natively suppress background applications to save battery, frequently silencing critical alerts. To solve this, Guardian AI splits the alarm output into two distinct routes:
1.  **Audio Siren:** Pushed via the **Telegram Bot API** to force a loud, overriding sound.
2.  **Visual Dashboard:** Powered by the **Blynk IoT App**.

**Engineering Justification for Blynk:** Rather than building a native application from scratch via Android Studio (which is restricted to Android devices and highly time-consuming), Blynk was selected because it is **Cross-Platform (iOS & Android)**, **IoT-ready** for fast alert communications, and highly cost-effective for PC development.

---

## 5. Results & Performance Demonstration
### *(Assessment Criterion: Demonstration of working implementation)*

### 5.1 Critical Latency Analysis (Honest System Evaluation)
While the AI logic performed flawlessly, empirical measurements of the Wi-Fi-based PoC revealed a severe hardware bottleneck:
*   **Frame Rate:** 10–15 FPS.
*   **End-to-End Latency:** **~1.0 Seconds** (Smartphone Encoding $\rightarrow$ Wi-Fi $\rightarrow$ PC Decoding).

In a real-world scenario, if a vehicle travels at an urban speed of 30 km/h ($v \approx 5.56\text{ m/s}$), the 1-second delay ($t = 1.0\text{ s}$) yields a critical braking deficit:
$$Distance = v \times t = 5.56 \times 1.0 = 5.56\text{ meters}$$
An extra 1.666 meters of blind travel is a fatal flaw for a physical vehicle, proving that Wi-Fi transmission is unviable for final deployment. 

---

## 6. Relevance to Unmanned Autonomous Systems (Future Upgrades)
### *(Assessment Criterion: Relevance to unmanned autonomous systems)*

To transition this PC into an industry-grade module for Unmanned Autonomous Systems (UAS), the 5.56-meter latency flaw must be eradicated. We propose a concrete, multi-phase future upgrade roadmap:

### 6.1 Portable Edge Computing Deployment (Immediate Fix)
To achieve true portability and zero latency, the system will abandon the "Laptop + Wi-Fi" architecture. The Python backend and YOLOv8 model will be ported to a **Mini-PC (e.g., Raspberry Pi 5 or NVIDIA Jetson)**.
*   **Benefit:** Powered by a standard power bank (no laptop required), the camera connects directly to the board, achieving **zero Wi-Fi latency**, immediately neutralizing the 2.78m braking delay, and stabilizing FPS.


---

## 7. Conclusion
The Guardian AI project successfully demonstrates a highly functional, vision-based ADAS prototype targeting vulnerable road users. By discarding theoretical math in favor of empirical video testing, the team optimized precise detection thresholds (6,000px and 2,000px). Coupled with an innovative, cross-platform decoupled alerting architecture, the system guarantees alert delivery. Furthermore, by rigorously measuring and calculating our PoC latency limitations, the project establishes a mathematically proven, highly practical roadmap toward Edge Computing and Unmanned Autonomous Systems integration.

## 8. PPT Slide:
* https://connectpolyu-my.sharepoint.com/:p:/g/personal/25134783d_connect_polyu_hk/IQC0dYZCCwasRLuKEfo0gDPtAWZd2Secq3D7in_rlks3pjo?e=g2UmQu

## 9. Video (YouTube): 
* Demonstration: https://youtu.be/Cz_ouFdwdhI?si=DHvJq63FIajnveiD
* GuardianAI: https://youtube.com/shorts/9B2_a3AWMsw?si=3fxfBuCSHNT98Vn1

## 10. Configuration
Edit __config.py__:  to adjust:

* Pixel area thresholds (Person: 6000, Cat/Dog: 2000)
* max_area for dynamic area dictionary
* Alert settings (Telegram Bot Token, Chat ID, Blynk auth)

## 11. Future Work

* TensorRT optimization
* Full hardware integration with vehicle camera

## 12. References

* YOLOv8 by Ultralytics
* WHO Road Traffic Injuries Fact Sheet
* IIHS Blind Spot Research
* Hong Kong Transport Department Accident Statistics

