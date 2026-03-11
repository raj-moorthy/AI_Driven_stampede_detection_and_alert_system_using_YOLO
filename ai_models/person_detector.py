"""
person_detector.py
Wraps YOLO person detection for standalone use.
"""
from ultralytics import YOLO

_model = None

def _get_model():
    global _model
    if _model is None:
        _model = YOLO("yolov8n.pt")
    return _model


def detect_people(frame):
    """
    Detects people in the given frame using YOLOv8.

    Args:
        frame (np.ndarray): BGR frame.

    Returns:
        list: List of bounding boxes [x1, y1, x2, y2] for detected persons.
    """
    model = _get_model()
    results = model(frame)
    person_boxes = []

    if results and hasattr(results[0], "boxes") and results[0].boxes is not None:
        boxes = results[0].boxes
        if hasattr(boxes, "data"):
            data = boxes.data.cpu().numpy()
            person_boxes = [box[:4].tolist() for box in data if int(box[5]) == 0]

    return person_boxes
