Gaze - Webcam Eye-tracking + Focus Notification Prototype

detects focus loss via webcam (MediaPipe) and triggers
browser notifications through a Chrome extension. It also serves a local dashboard that shows a live
focus status indicator (green = focused, red = distracted).

Folder contents:
- app/server.py          : Flask server to receive eye-tracker updates and serve status/dashboard
- eye_tracker.py        : MediaPipe-based webcam eye-tracker that POSTs status to server
- requirements.txt      : Python dependencies
- extension/manifest.json
- extension/background.js
- extension/options.html
- extension/icon.png    : placeholder icon
- README_INSTALL.md     : step-by-step install & run instructions

summary:
1) Start Flask server: python3 app/server.py
2) Start eye tracker: python3 eye_tracker.py
3) Load the Chrome extension (Developer mode -> Load unpacked -> select extension/)
4) Open http://127.0.0.1:5000 in Chrome to view dashboard (optional)
