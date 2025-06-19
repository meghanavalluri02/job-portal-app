from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL connection config
db_config = {
    "host": "mysql",  # Kubernetes service name
    "user": "root",
    "password": "password",
    "database": "jobportal"
}

@app.route("/applications", methods=["GET"])
def get_applications():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.id, a.applicant_name, a.resume, j.title AS job_title, j.company
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
        """)
        applications = cursor.fetchall()
        conn.close()
        return jsonify(applications)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/applications", methods=["POST"])
def apply_to_job():
    data = request.get_json()
    job_id = data.get("job_id")
    applicant_name = data.get("applicant_name")
    resume = data.get("resume")

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO applications (job_id, applicant_name, resume) VALUES (%s, %s, %s)",
                       (job_id, applicant_name, resume))
        conn.commit()
        conn.close()
        return jsonify({"message": "Application submitted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
