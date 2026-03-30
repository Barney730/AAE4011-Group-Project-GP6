# utils/dynamic_area.py
import cv2

def get_dynamic_max_area(frame_shape, setting='medium'):
    """Return max_area based on frame size and chosen setting"""
    height, width = frame_shape[:2]
    frame_area = height * width
    
    settings = {
        'small': 10000,
        'medium': 50000,
        'large': 200000
    }
    return min(settings.get(setting, 50000), frame_area // 4)

def should_trigger_alert(area, class_id):
    """Empirical threshold check"""
    if class_id == 0:        # Person
        return area >= 6000
    elif class_id in [15, 16]:  # Cat or Dog
        return area >= 2000
    return False
