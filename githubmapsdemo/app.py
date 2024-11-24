from flask import Flask, render_template, request, jsonify
import webbrowser
from threading import Timer
from datetime import datetime, timedelta
import threading

app = Flask(__name__)

# Placeholder for event data storage
events = []

@app.route('/')
def home():
    # Renders the HTML file from the "templates" folder
    return render_template('eventhtmlfile.html')

@app.route('/add_event', methods=['POST'])
def add_event():
    """ Endpoint to add an event to the storage """
    data = request.get_json()

    if not data or 'title' not in data or 'time' not in data:
        return jsonify({'error': 'Invalid input data. Please provide both title and time.'}), 400

    try:
        event_name = data['title']
        event_time = datetime.strptime(data['time'], '%Y-%m-%dT%H:%M:%S')

        events.append({'name': event_name, 'time': event_time})

        # Schedule alert exactly one hour before event
        alert_time = event_time - timedelta(hours=1)
        delay = (alert_time - datetime.now()).total_seconds()

        if delay > 0:
            threading.Timer(delay, send_alert, args=[event_name, event_time]).start()

        return jsonify({'message': 'Event added successfully!'}), 200
    except ValueError:
        return jsonify({'error': 'Invalid time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400

def send_alert(event_name, event_time):
    """ Function to send an alert one hour before the event """
    print(f"Alert: Your event '{event_name}' is scheduled at {event_time}. Please prepare accordingly.")

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    # Automatically open the browser after a short delay
    Timer(1, open_browser).start()
    app.run(debug=True,use_reloader=False)
