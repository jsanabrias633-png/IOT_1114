from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

sensor_data = {"temperature": None, "humidity": None}

@app.route("/")
def index():
    return render_template("index.html", data=sensor_data)

@app.route("/update", methods=["POST"])
def update():
    global sensor_data
    content = request.get_json()
    if content:
        sensor_data["temperature"] = content.get("temperature")
        sensor_data["humidity"] = content.get("humidity")
    return jsonify({"status": "success", "data": sensor_data})

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(sensor_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
