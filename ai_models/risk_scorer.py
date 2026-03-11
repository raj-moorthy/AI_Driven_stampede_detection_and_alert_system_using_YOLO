"""
risk_scorer.py
Calculates a composite risk level from density, motion, pose, and crowd size.
"""


def calculate_risk_score(density_score: float, motion_score: float,
                          pose_score: bool, num_people: int) -> str:
    """
    Returns a risk level string: 'High', 'Medium', or 'Low'.

    Weights:
        - density_score : 0.0-1.0  (40%)
        - motion_score  : 0.0-1.0  (30%)
        - pose_score    : bool      (20% — True if fall detected)
        - num_people    : int       (10% — normalised at 30 persons)

    Returns:
        str: 'High' | 'Medium' | 'Low'
    """
    people_score = min(1.0, num_people / 30.0)
    pose_val = 1.0 if pose_score else 0.0

    composite = (
        0.40 * density_score +
        0.30 * motion_score  +
        0.20 * pose_val      +
        0.10 * people_score
    )

    if composite >= 0.6:
        return "High"
    elif composite >= 0.35:
        return "Medium"
    else:
        return "Low"
