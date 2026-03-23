import sqlite3

conn = sqlite3.connect("dialysis.db")
cursor = conn.cursor()

# ==========================
# CREATE DIALYSIS TABLE
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS dialysis_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    age INTEGER,
    gender TEXT,
    weight REAL,
    
    diabetes INTEGER,
    hypertension INTEGER,
    
    creatinine REAL,
    urea REAL,
    potassium REAL,
    
    hemoglobin REAL,
    ktv REAL,
    urr REAL,
    
    prediction TEXT,
    date TEXT
)
""")

# ==========================
# CREATE USERS TABLE 🔐
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# ==========================
# INSERT DEFAULT USER
# ==========================
cursor.execute("""
INSERT OR IGNORE INTO users (username, password)
VALUES (?, ?)
""", ("admin", "admin123"))

# ==========================
# SAVE & CLOSE
# ==========================
conn.commit()
conn.close()

print("✅ VitalSense database & user table created successfully!")