from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# =========================
# CREATE DATABASE & TABLE
# =========================
conn = sqlite3.connect('vitalsense.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    heart_rate INTEGER,
    blood_pressure INTEGER,
    temperature INTEGER,
    oxygen INTEGER,
    status TEXT
)
''')

conn.commit()
conn.close()

# =========================
# HOME PAGE (LOGIN PAGE)
# =========================
@app.route('/')
def home():
    return render_template('login.html')

# =========================
# LOGIN
# =========================
@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "1234":
        return redirect('/dashboard')   # ✅ redirect instead of render
    else:
        return "Invalid Username or Password"

# =========================
# DASHBOARD
# =========================
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if request.method == 'POST':

        heart_rate = int(request.form['heart_rate'])
        blood_pressure = int(request.form['blood_pressure'])
        temperature = int(request.form['temperature'])
        oxygen = int(request.form['oxygen'])

        status = "Healthy ✅"

        if (heart_rate < 60 or heart_rate > 100 or
            blood_pressure < 90 or blood_pressure > 120 or
            temperature < 97 or temperature > 99 or
            oxygen < 95):

            status = "⚠ Abnormal! Please Consult Doctor"

        conn = sqlite3.connect('vitalsense.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO health_records
        (heart_rate, blood_pressure, temperature, oxygen, status)
        VALUES (?, ?, ?, ?, ?)
        ''', (heart_rate, blood_pressure, temperature, oxygen, status))

        conn.commit()
        conn.close()

        return render_template(
            'dashboard.html',
            heart_rate=heart_rate,
            blood_pressure=blood_pressure,
            temperature=temperature,
            oxygen=oxygen,
            status=status
        )

    return render_template('dashboard.html')

# =========================
# RECORDS PAGE (GRAPH PAGE)
# =========================
@app.route('/records')
def records():
    conn = sqlite3.connect('vitalsense.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM health_records")
    data = cursor.fetchall()

    ids = [row[0] for row in data]
    heart_rates = [row[1] for row in data]
    blood_pressures = [row[2] for row in data]
    temperatures = [row[3] for row in data]
    oxygen_levels = [row[4] for row in data]

    conn.close()

    return render_template(
        'records.html',
        records=data,
        ids=ids,
        heart_rates=heart_rates,
        blood_pressures=blood_pressures,
        temperatures=temperatures,
        oxygen_levels=oxygen_levels
    )

# =========================
# DELETE RECORD
# =========================
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('vitalsense.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM health_records WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect('/records')


if __name__ == '__main__':
    app.run(debug=True)