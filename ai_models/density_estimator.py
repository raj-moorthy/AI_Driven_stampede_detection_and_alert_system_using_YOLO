"""
density_estimator.py
Generates a density heatmap and score from a list of detected person bounding boxes.
"""
import cv2
import numpy as np


def generate_density_heatmap(frame, person_boxes):
    """
    Overlays a Gaussian heatmap on the frame and returns a density score.

    Args:
        frame (np.ndarray): BGR frame from OpenCV.
        person_boxes (list): List of bounding boxes [x1, y1, x2, y2].

    Returns:
        tuple: (frame_with_heatmap: np.ndarray, density_score: float 0.0-1.0)
    """
    h, w = frame.shape[:2]
    heatmap = np.zeros((h, w), dtype=np.float32)

    for box in person_boxes:
        x1, y1, x2, y2 = [int(c) for c in box]
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        radius = max(int((x2 - x1 + y2 - y1) / 4), 20)

        # Draw a Gaussian blob at the person's centroid
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < w and 0 <= ny < h:
                    dist = (dx ** 2 + dy ** 2) ** 0.5
                    heatmap[ny, nx] += max(0, 1 - dist / radius)

    # Normalize heatmap
    if heatmap.max() > 0:
        heatmap /= heatmap.max()

    # Density score: weighted by number of people and their spread
    density_score = min(1.0, len(person_boxes) / 30.0)

    # Colour-map and blend
    heatmap_u8 = (heatmap * 255).astype(np.uint8)
    colored = cv2.applyColorMap(heatmap_u8, cv2.COLORMAP_JET)
    blended = cv2.addWeighted(frame, 0.65, colored, 0.35, 0)

    return blended, density_score
