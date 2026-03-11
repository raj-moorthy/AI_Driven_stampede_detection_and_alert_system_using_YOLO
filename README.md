**Safe Muster – Human Stampede Early Warning System**
Safe Muster is an AI-powered system designed to prevent stampede disasters in high-density public gatherings like religious festivals, concerts, or political rallies. By using CCTV footage or webcam input, it detects crowd density, identifies fall patterns, and predicts potential stampede risk using deep learning techniques like YOLOv8, OpenPose, Optical Flow, and ConvLSTM.

**Features**
Real-time person detection using YOLOv8
Density heatmap generation
Fall and abnormal pose detection using OpenPose
Motion analysis via optical flow
ConvLSTM-based risk score prediction
Phone call alert to nearest police station when high risk is detected
Frontend built with Flask, HTML, and CSS
Prototype demo with webcam or video upload

**Tech Stack**
Person Detection :	YOLOv8 (Ultralytics)
Pose Estimation	: OpenPose
Motion Detection :	Optical Flow (Farneback)
Risk Prediction :	ConvLSTM (Keras/TensorFlow)
Web Interface :	Flask (Frontend), Gradio for HF
Deployment :	Render

**Alert System**
The system integrates:
Overpass API for nearest police station detection
Twilio API for automated voice call alerts when stampede risk is high

**Future Enhancements**
Mobile app integration
On-edge deployment in smart cameras
Multi-angle CCTV fusion
Multilingual audio alerts
Real-time drone monitoring
