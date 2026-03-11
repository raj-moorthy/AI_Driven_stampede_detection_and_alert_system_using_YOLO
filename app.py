import gradio as gr
import cv2
import tempfile

from ai_models.person_detector import PersonDetector
from ai_models.density_estimator import DensityEstimator
from ai_models.motion_analyzer import MotionAnalyzer
from ai_models.risk_scorer import RiskScorer

# Initialize modules
person_detector = PersonDetector()
density_estimator = DensityEstimator()
motion_analyzer = MotionAnalyzer()
risk_scorer = RiskScorer()


def process_video(video_path):

    cap = cv2.VideoCapture(video_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    temp_output = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(temp_output.name, fourcc, fps, (width, height))

    prev_frame = None

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        # 1️⃣ Detect people
        persons = person_detector.detect(frame)

        # 2️⃣ Estimate crowd density
        density = density_estimator.estimate(persons, frame)

        # 3️⃣ Analyze crowd motion
        motion = motion_analyzer.analyze(prev_frame, frame)

        # 4️⃣ Compute risk score
        risk = risk_scorer.compute(density, motion)

        # Draw results
        for box in persons:
            x1, y1, x2, y2 = box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

        cv2.putText(
            frame,
            f"Risk Level: {risk}",
            (30,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            3
        )

        out.write(frame)
        prev_frame = frame

    cap.release()
    out.release()

    return temp_output.name


demo = gr.Interface(
    fn=process_video,
    inputs=gr.Video(label="Upload Crowd Video"),
    outputs=gr.Video(label="Detection Result"),
    title="AI Driven Stampede Detection System",
    description="Upload a crowd video to detect potential stampede risks using AI."
)

demo.launch(server_name="0.0.0.0", server_port=7860)