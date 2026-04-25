installation instructions--

terminal :

cd Desktop/filename

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt

python3 app/server.py


server runs at http://127.0.0.1:5000/

In a separate terminal but under the venv, run the eye tracker: python3 eye_tracker.py USERNAME

This opens a webcam window; press 'q' to quit.
remember to include username, i.e. 'Alaina' or it will default to default_user and eye_tracker data will not record to CSV
Other troubleshooting:

On macOS give permissions to Chrome for notifications/sound + make sure Focus/DnD is off
