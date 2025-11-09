Installation & Run Instructions (macOS)

1) Unzip Gaze_package.zip and open a terminal in the folder (cd Desktop/Gaze_package)

2) Create & activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate   (macOS/Linux)

3) Install dependencies:
   pip install -r requirements.txt

4) Start the Flask server (in a terminal):
   python3 app/server.py
   Server runs at http://127.0.0.1:5000/

5) In a separate terminal but under the venv, run the eye tracker:
   python3 eye_tracker.py
   This opens a webcam window; press 'q' to quit.

6) Install Chrome extension:
   - Open chrome://extensions/
   - Enable Developer mode
   - Click 'Load unpacked' and choose the 'extension' folder inside the package.
   - The extension polls the local server and sends notifications.

7) Open the dashboard at http://127.0.0.1:5000 to see the live focus status.

Troubleshooting:
- If MediaPipe install fails, ensure pip is up to date and Python version >=3.8.
- If webcam access is blocked, grant permission through system settings and ensure no other app uses the camera. Also try running command: tccutil reset Camera. then rerun the script so it prompts you for permission with a popup (Mac).
