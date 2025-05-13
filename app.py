from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify

from api import schedule_validation, start_unifi_listener

import threading

t = threading.Thread(target=start_unifi_listener, daemon=True)
t.start()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/webuntis/present", methods=["GET", "POST"])
def webuntis_present():
    """
    Called by WebUntis UI button:
      e.g. https://our-server/webuntis/present?user=student123
    """

    user = request.values.get("user")
    if not user:
        return jsonify({"error": "missing user"}), 400
    
    # Schedule validation in 10 minutes
    schedule_validation(user, delay_minutes=10)
    return jsonify({"status": "scheduled", "user": user})

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)