import os
import json
import pytesseract
import cv2
import psycopg2
from pdf2image import convert_from_path
from datetime import datetime

# Database connection
DB_CONFIG = {
    "dbname": "ocr_db",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

# OCR Processing
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extract_text_from_image(image_path):
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image)
    return text

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    extracted_text = ""
    for i, image in enumerate(images):
        temp_image_path = f"temp_page_{i}.jpg"
        image.save(temp_image_path, "JPEG")
        extracted_text += extract_text_from_image(temp_image_path) + "\n"
        os.remove(temp_image_path)
    return extracted_text

# Parse extracted text into structured JSON
def parse_extracted_text(text):
    lines = text.split("\n")
    parsed_data = {
        "patient_name": "", "dob": "", "date": "",
        "injection": "", "exercise_therapy": "",
        "difficulty_ratings": {}, "pain_symptoms": {},
        "medical_assistant_data": {}
    }
    
    for line in lines:
        if "Patient Name" in line:
            parsed_data["patient_name"] = line.split(":")[-1].strip()
        elif "DOB" in line:
            parsed_data["dob"] = line.split(":")[-1].strip()
        elif "INJECTION" in line:
            parsed_data["injection"] = "Yes" if "YES" in line else "No"
        elif "Exercise Therapy" in line:
            parsed_data["exercise_therapy"] = "Yes" if "YES" in line else "No"
        elif "Pain:" in line:
            values = [int(num) for num in line.split() if num.isdigit()]
            if len(values) >= 5:
                parsed_data["pain_symptoms"] = {"pain": values[0], "numbness": values[1], "tingling": values[2], "burning": values[3], "tightness": values[4]}
        elif "Blood Pressure" in line:
            parsed_data["medical_assistant_data"]["blood_pressure"] = line.split(":")[-1].strip()
    
    parsed_data["date"] = datetime.now().strftime("%Y-%m-%d")
    return parsed_data

# Store data in PostgreSQL
def store_data_in_db(data):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("INSERT INTO patients (name, dob) VALUES (%s, %s) RETURNING id", (data["patient_name"], data["dob"]))
        patient_id = cur.fetchone()[0]
        cur.execute("INSERT INTO forms_data (patient_id, form_json) VALUES (%s, %s)", (patient_id, json.dumps(data)))
        conn.commit()
        cur.close()
        conn.close()
        print("Data stored successfully!")
    except Exception as e:
        print("Database error:", e)

# Main execution
def main(file_path):
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_image(file_path)
    structured_data = parse_extracted_text(text)
    with open("output.json", "w") as f:
        json.dump(structured_data, f, indent=4)
    store_data_in_db(structured_data)

if __name__ == "__main__":
    main("sample_form.pdf")
