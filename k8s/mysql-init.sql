CREATE DATABASE IF NOT EXISTS jobportal;
USE jobportal;

CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    company VARCHAR(100),
    location VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT,
    applicant_name VARCHAR(100),
    resume TEXT,
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);
