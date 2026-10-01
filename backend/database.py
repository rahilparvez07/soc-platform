import sqlite3
from datetime import datetime

DATABASE = "../soc.db"


def create_database():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            rule TEXT NOT NULL,
            severity TEXT NOT NULL,
            source_ip TEXT,
            failed_attempts INTEGER,
            description TEXT,
            mitre_attack TEXT,
            status TEXT DEFAULT 'New'
        )
    """)

    connection.commit()
    connection.close()


def save_alert(alert):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO alerts (
            timestamp,
            rule,
            severity,
            source_ip,
            failed_attempts,
            description,
            mitre_attack,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        alert["rule"],
        alert["severity"],
        alert["source_ip"],
        alert["failed_attempts"],
        alert["description"],
        alert["mitre_attack"],
        "New"
    ))

    connection.commit()
    connection.close()