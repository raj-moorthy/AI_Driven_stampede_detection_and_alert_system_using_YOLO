from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run_detection", methods=["POST"])
def run_detection():
    try:
        subprocess.run(["python", "main_pipeline.py"])
        return {"status": "Detection started"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)