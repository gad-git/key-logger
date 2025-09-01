from flask import Flask, request

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log_key():
    data = request.get_json()
    print("Получено:", data)
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
