"""
pose_estimator.py
Detects falls or abnormal poses using MediaPipe Pose.
"""
import cv2

try:
    import mediapipe as mp
    _mp_pose = mp.solutions.pose
    _pose = _mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
    _MP_AVAILABLE = True
except Exception:
    _MP_AVAILABLE = False

def detect_pose_fall(frame):
    """
    Analyses the frame for fallen / horizontal poses.

    Args:
        frame (np.ndarray): BGR frame.

    Returns:
        bool: True if a fall-like pose is detected.
    """
    if not _MP_AVAILABLE:
        return False

    try:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = _pose.process(rgb)

        if not results.pose_landmarks:
            return False

        lm = results.pose_landmarks.landmark
        # Key landmark indices: LEFT_SHOULDER=11, RIGHT_SHOULDER=12
        #                       LEFT_HIP=23,      RIGHT_HIP=24
        shoulder_y = (lm[11].y + lm[12].y) / 2
        hip_y      = (lm[23].y + lm[24].y) / 2

        # If shoulders are at or below hip level → person is likely horizontal
        height_diff = abs(shoulder_y - hip_y)
        fall_detected = height_diff < 0.12  # threshold tuned empirically

        return bool(fall_detected)

    except Exception as e:
        print("Pose estimation error:", e)
        return False
