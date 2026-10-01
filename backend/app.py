from flask import Flask, jsonify, send_from_directory, request
import sqlite3
import os
app = Flask(__name__)


DATABASE = "../soc.db"

FRONTEND_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../frontend")
)


def get_alerts():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM alerts
        ORDER BY id DESC
    """)

    alerts = cursor.fetchall()

    connection.close()

    return [dict(alert) for alert in alerts]


@app.route("/")
def home():
    return send_from_directory(FRONTEND_FOLDER, "index.html")


@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_FOLDER, filename)


@app.route("/api/alerts")
def alerts():
    return jsonify(get_alerts())
@app.route("/api/alerts/<int:alert_id>")
def get_alert(alert_id):

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM alerts WHERE id = ?",
        (alert_id,)
    )

    alert = cursor.fetchone()

    connection.close()

    if alert is None:
        return jsonify({"error": "Alert not found"}), 404

    return jsonify(dict(alert))

@app.route("/api/alerts/<int:alert_id>/status", methods=["PUT"])
def update_alert_status(alert_id):

    data = request.get_json()

    status = data.get("status")

    allowed_statuses = [
        "New",
        "Investigating",
        "Resolved"
    ]

    if status not in allowed_statuses:
        return jsonify({
            "error": "Invalid status"
        }), 400


    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE alerts
        SET status = ?
        WHERE id = ?
        """,
        (status, alert_id)
    )

    connection.commit()

    updated = cursor.rowcount

    connection.close()


    if updated == 0:

        return jsonify({
            "error": "Alert not found"
        }), 404


    return jsonify({
        "message": "Alert status updated",
        "status": status
    })


if __name__ == "__main__":
    app.run(debug=False)