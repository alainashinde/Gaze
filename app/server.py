from flask import Flask, jsonify, request, send_from_directory, render_template
from datetime import datetime
import csv, os

app = Flask(__name__, template_folder='templates', static_folder='static')
STATE = {'focused': True, 'last_updated': None}
LOGFILE = os.path.join(os.getcwd(), 'events.csv')

def log_event(event, info=''):
    ts = datetime.utcnow().isoformat()
    header = not os.path.exists(LOGFILE)
    with open(LOGFILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(['timestamp','event','info'])
        writer.writerow([ts,event,info])

@app.route('/status', methods=['GET'])
def status():
    return jsonify(STATE)

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json() or {}
    focused = bool(data.get('focused', True))
    STATE['focused'] = focused
    STATE['last_updated'] = datetime.utcnow().isoformat()
    log_event('eye_update', str(focused))
    return jsonify({'ok': True})

@app.route('/events.csv', methods=['GET'])
def get_csv():
    if os.path.exists(LOGFILE):
        return send_from_directory(os.getcwd(), 'events.csv', as_attachment=True)
    else:
        return ('No log yet', 404)

@app.route('/', methods=['GET'])
def index():
    # Simple dashboard page
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
