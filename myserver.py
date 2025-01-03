from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Server is running!"

# ฟังก์ชันที่ใช้ในการเริ่มต้นเซิร์ฟเวอร์
def run_flask_server():
    app.run(host='0.0.0.0', port=8080)

# ฟังก์ชัน start_server ที่ใช้รันฟังก์ชัน run_flask_server ใน Thread
def start_server():
    t = Thread(target=run_flask_server)  # ใช้ target=run_flask_server แทน
    t.start()

# เรียกใช้ฟังก์ชันเพื่อเริ่มต้นเซิร์ฟเวอร์
start_server()
