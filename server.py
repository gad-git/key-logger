from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

logs = []

@app.route('/log', methods=['POST'])
def log_key():
    data = request.get_json()
    logs.append(data)
    print("received:", data)
    return {"status": "ok"}

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(logs)

@app.route('/')
def index():
    return render_template('index.html')  # rendering file from templates

if __name__ == '__main__':
    app.run(debug=True, port=5000)
