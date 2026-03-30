# Guardian AI Configuration - Matches empirical calibration in report

# Empirical Pixel Thresholds (from video testing at 3.0m danger zone)
PERSON_THRESHOLD = 6000      # Class 0: Person
CAT_THRESHOLD = 2000         # Class 15: Cat
DOG_THRESHOLD = 2000         # Class 16: Dog

# Dynamic max_area settings (tested range)
MAX_AREA_SETTINGS = {
    'small': 10000,
    'medium': 50000,   # Recommended balanced value for blind-spot coverage
    'large': 200000
}

# Target COCO classes
TARGET_CLASSES = [0, 15, 16]   # person, cat, dog

# Detection parameters
CONFIDENCE_THRESHOLD = 0.45
IOU_THRESHOLD = 0.45

# Alert settings (replace with your own)
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

# Blynk (legacy support - consider MQTT for production)
BLYNK_AUTH_TOKEN = "YOUR_BLYNK_AUTH_TOKEN_HERE"
BLYNK_VIRTUAL_PIN = 1   # For visual alert

# Video / Camera
CAMERA_SOURCE = 0       # 0 for webcam, or video file path
