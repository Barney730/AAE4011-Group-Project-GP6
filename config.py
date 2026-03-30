# Guardian AI Configuration
PERSON_THRESHOLD = 6000      # pixels - optimized for 3.0m danger zone
CAT_THRESHOLD = 2000         # pixels
DOG_THRESHOLD = 2000         # pixels

# Dynamic Area Dictionary - max_area for processing regions
MAX_AREA_SETTINGS = {
    'small': 10000,
    'medium': 50000,     # Recommended balanced value
    'large': 200000
}

# Alert Settings
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
BLYNK_AUTH_TOKEN = "YOUR_BLYNK_TOKEN"

# Detection Classes (COCO)
TARGET_CLASSES = [0, 15, 16]  # Person, Cat, Dog

# Video / Camera Settings
CONFIDENCE_THRESHOLD = 0.45
