from flask import Flask, request, render_template, send_file, redirect, url_for
import os
import csv
from werkzeug.utils import secure_filename
from src.helper import llm_pipeline

app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_file.pdf'
CSV_FOLDER = os.path.join('static', 'csv_files')
os.makedirs(CSV_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return render_template("error.html", message="No file part in the request.")

    file = request.files['file']

    if file.filename == '':
        return render_template("error.html", message="No selected file.")

    filename = secure_filename("uploaded_file.pdf")
    file_path = os.path.join(".", filename)
    file.save(file_path)

    try:
        result = llm_pipeline(file_path)
        response_data = {
            "status": "success",
            "data": result
        }
    except Exception as e:
        response_data = {
            "status": "error",
            "message": str(e)
        }

    return render_template("result.html", response_data=response_data)

def get_csv(file_path):
    answer_generation_chain, ques_list = llm_pipeline(file_path)
    csv_file_path = os.path.join(CSV_FOLDER, "output.csv")
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Question", "Answer"])
        for question in ques_list:
            answer = answer_generation_chain.run(question)
            writer.writerow([question, answer])
    return csv_file_path

@app.route("/download_csv", methods=["GET"])
def download_csv():
    try:
        csv_file_path = get_csv(UPLOAD_FOLDER)
        return render_template("download.html", csv_file_path=csv_file_path)
    except Exception as e:
        return render_template("error.html", message=str(e))

@app.route("/download", methods=["GET"])
def download_file():
    csv_file_path = os.path.join(CSV_FOLDER, "output.csv")
    if os.path.exists(csv_file_path):
        return send_file(csv_file_path, as_attachment=True)
    else:
        return render_template("error.html", message="CSV file not found.")

if __name__ == "__main__":
    app.run(debug=True)
