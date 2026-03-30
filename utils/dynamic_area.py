# utils/dynamic_area.py
def get_dynamic_max_area(frame_shape, setting='medium'):
    """Return appropriate max_area based on frame size and chosen setting"""
    height, width = frame_shape[:2]
    frame_area = height * width
    
    settings = {
        'small': 10000,
        'medium': 50000,
        'large': 200000
    }
    chosen = settings.get(setting, 50000)
    return min(chosen, frame_area // 4)  # Prevent overly large areas

def should_trigger_alert(area: float, class_id: int) -> bool:
    """Empirical threshold check from video calibration"""
    if class_id == 0:        # Person
        return area >= 6000
    elif class_id == 15 or class_id == 16:  # Cat or Dog
        return area >= 2000
    return False

def get_class_label(class_id: int) -> str:
    labels = {0: "Person", 15: "Cat", 16: "Dog"}
    return labels.get(class_id, "Unknown")
