# OCR Data Extraction and Storage

## Project Overview
This project automates data extraction from scanned patient assessment forms using Optical Character Recognition (OCR) and stores structured data in a SQL database.

## Features
- Extracts text from PDFs and images using *Tesseract OCR*
- Parses key fields into structured JSON format
- Stores extracted data in a *PostgreSQL database*
- Supports handwritten and printed text
- Preprocessing techniques to enhance OCR accuracy

## Setup Instructions
### Prerequisites
- Python 3.8+
- PostgreSQL installed and running
- Tesseract-OCR installed (Add to system path)
- Required Python libraries: pytesseract, opencv-python, pdf2image, psycopg2

### Installation Steps
1. *Clone the repository:*
   sh
   git clone https://github.com/your-repo/ocr-data-pipeline.git
   cd ocr-data-pipeline
   

2. *Install dependencies:*
   sh
   pip install -r requirements.txt
   

3. *Set up the database:*
   sh
   psql -U postgres -f database_schema.sql
   
   If needed, create the database manually:
   sql
   CREATE DATABASE ocr_db;
   

4. *Run the OCR extraction script:*
   sh
   python main.py sample_form.pdf
   

## Project Structure

ocr-data-pipeline/
│-- main.py               # OCR processing and database storage script
│-- database_schema.sql   # SQL script for database setup
│-- requirements.txt      # Required dependencies
│-- README.md             # Documentation
│-- output.json           # Sample extracted JSON output
│-- sample_form.pdf       # Example patient assessment form


## Sample JSON Output
json
{
  "patient_name": "John Doe",
  "dob": "1988-05-01",
  "date": "2025-06-02",
  "injection": "Yes",
  "exercise_therapy": "No",
  "difficulty_ratings": {
    "bending": 3,
    "putting_on_shoes": 1,
    "sleeping": 2
  },
  "pain_symptoms": {
    "pain": 2,
    "numbness": 5
  },
  "medical_assistant_data": {
    "blood_pressure": "120/80",
    "hr": 80
  }
}


## Database Schema
sql
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    dob DATE NOT NULL
);

CREATE TABLE forms_data (
    id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(id) ON DELETE CASCADE,
    form_json JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);


## How to Contribute
1. Fork the repository.
2. Create a feature branch (git checkout -b feature-branch).
3. Commit your changes (git commit -m "Add new feature").
4. Push to your branch (git push origin feature-branch).
5. Open a Pull Request.

## License
This project is open-source and free to use under the MIT license.
