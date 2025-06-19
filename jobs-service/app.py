from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL config (update host if needed in K8s)
db_config = {
    "host": "mysql",  # Kubernetes service name
    "user": "root",
    "password": "password",
    "database": "jobportal"
}

@app.route("/jobs", methods=["GET"])
def get_jobs():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs")
        jobs = cursor.fetchall()
        conn.close()
        return jsonify(jobs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/jobs", methods=["POST"])
def add_job():
    data = request.get_json()
    title = data.get("title")
    company = data.get("company")
    location = data.get("location")

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jobs (title, company, location) VALUES (%s, %s, %s)",
                       (title, company, location))
        conn.commit()
        conn.close()
        return jsonify({"message": "Job added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
