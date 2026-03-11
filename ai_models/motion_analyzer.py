"""
motion_analyzer.py
Calculates a motion score by analysing optical flow between consecutive frames.
"""
import cv2
import numpy as np


def calculate_motion_score(prev_frame, curr_frame):
    """
    Computes a normalised motion score using dense optical flow (Farneback).

    Args:
        prev_frame (np.ndarray): Previous BGR frame.
        curr_frame (np.ndarray): Current BGR frame.

    Returns:
        float: Motion score between 0.0 (no motion) and 1.0 (extreme motion).
    """
    try:
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(
            prev_gray, curr_gray,
            None,
            pyr_scale=0.5, levels=3, winsize=15,
            iterations=3, poly_n=5, poly_sigma=1.2,
            flags=0
        )

        magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        mean_mag = float(np.mean(magnitude))

        # Normalise: 20px/frame ≈ very high motion
        motion_score = min(1.0, mean_mag / 20.0)
        return round(motion_score, 4)

    except Exception as e:
        print("Motion analysis error:", e)
        return 0.0
