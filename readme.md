Computer vision-based focus tracking platform using MediaPipe Face Mesh, OpenCV, and customizable browser-monitoring Chrome extension and notifications to detect attention shifts during online work.

[https://chromewebstore.google.com/detail/gaze/gnfdmeanclbepmgbenmdkojeemdcfmep](url)



server runs at http://127.0.0.1:5000/

Troubleshooting for macOS:

- when running the eye tracker: remember to include username, i.e. 'Alaina' or it will default to default_user and eye_tracker data will not record to user-specific CSV (+ additional issues with connecting chrome notifs and eye tracker)

- On macOS give permissions to Chrome for notifications/sound & make sure Focus/DnD is off
