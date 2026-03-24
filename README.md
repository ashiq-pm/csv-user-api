# 📊 CSV User Upload API (Django REST Framework)

## 🚀 Overview

This project implements a robust and scalable **CSV Upload API** using Django REST Framework (DRF).
The API allows users to upload a CSV file containing user data, validates each record, and stores only valid entries in the database while providing a structured summary of the operation.

This solution focuses on **clean architecture, efficient data processing, validation, and performance optimization**, making it suitable for real-world backend systems.

---

## 🎯 Features

* 📁 Upload CSV files via REST API
* ✅ Field-level validation using DRF serializers
* 🔁 Graceful handling of duplicate email records
* 📊 Detailed response with:

  * Total records processed
  * Successfully saved records
  * Rejected records
  * Skipped duplicates
  * Row-level validation errors
* ⚡ Optimized performance using bulk database insertion
* 🛡️ Robust error handling (invalid file, wrong format, missing fields)
* 🧪 Unit tests covering critical scenarios

---

## 🛠️ Tech Stack

* **Python**
* **Django**
* **Django REST Framework**
* **SQLite (default database)**

---

## 📂 Project Structure

```id="g3p9xe"
csv-user-api/
│
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tests.py
│   ├── urls.py
│
├── csv_user_api/
│   ├── settings.py
│   ├── urls.py
│
├── sample_files/
│   ├── sample.csv
│   ├── sample_output.json
│   ├── test_results.png
│
├── requirements.txt
├── README.md
├── manage.py
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```id="3sp8wp"
git clone (https://github.com/ashiq-pm/csv-user-api)
cd csv-user-api
```

---

### 2️⃣ Create Virtual Environment

```id="8y7k9v"
python -m venv env
```

Activate environment:

* **Windows**

```id="bnk8rj"
env\Scripts\activate
```

* **Mac/Linux**

```id="y6sd6m"
source env/bin/activate
```

---

### 3️⃣ Install Dependencies

```id="q8n3wb"
pip install -r requirements.txt
```

---

### 4️⃣ Apply Migrations

```id="zjv2o9"
python manage.py migrate
```

---

### 5️⃣ Run Development Server

```id="7lgv6a"
python manage.py runserver
```

Server will start at:

```id="xk9a2m"
http://127.0.0.1:8000/
```

---

## 📡 API Endpoint

### 🔹 Upload CSV

**Endpoint:**

```id="r4s8xp"
/api/upload-csv/
```

**Method:**

```id="y2k7zm"
POST
```

**Content-Type:**

```id="f1k8zc"
multipart/form-data
```

---

## 📥 Request Format

Upload CSV file using form-data:

| Key  | Type | Description |
| ---- | ---- | ----------- |
| file | File | CSV file    |

---

## 📄 Sample CSV Input

```id="p8m3vb"
name,email,age
John Doe,john@example.com,25
Jane Doe,jane@example.com,30
Invalid User,invalidemail,200
,empty@example.com,22
Duplicate User,john@example.com,40
```

---

## 📤 Sample Response

```json id="h4n2kj"
{
  "status": "success",
  "total_records": 5,
  "saved_records": 2,
  "rejected_records": 2,
  "skipped_duplicates": 1,
  "errors": [
    {
      "row": 3,
      "data": {
        "name": "Invalid User",
        "email": "invalidemail",
        "age": "200"
      },
      "errors": {
        "email": ["Enter a valid email address."],
        "age": ["Age must be between 0 and 120"]
      }
    },
    {
      "row": 4,
      "data": {
        "name": "",
        "email": "empty@example.com",
        "age": "22"
      },
      "errors": {
        "name": ["This field may not be blank."]
      }
    }
  ]
}
```

---

## ✅ Validation Rules

* **name** → Must be a non-empty string
* **email** → Must be a valid email format
* **age** → Must be between 0 and 120

---

## 🔁 Duplicate Handling

* Duplicate emails are **not treated as errors**
* They are **gracefully skipped**
* Count is returned in `skipped_duplicates`

---

## ⚡ Performance Optimization

* Uses `bulk_create()` for efficient database insertion
* Minimizes database queries using in-memory email tracking (`set`)
* Suitable for handling large CSV files

---

## 🛡️ Error Handling

The API handles:

* ❌ Missing file upload
* ❌ Invalid file type (non-CSV)
* ❌ Invalid CSV structure
* ❌ Missing required headers
* ❌ Row-level validation errors

---

## 🧪 Unit Testing

Unit tests are implemented using Django REST Framework’s testing tools.

### ✔ Covered Scenarios

* Valid and invalid data processing
* Duplicate email handling
* Invalid file type validation

---

### ▶️ Run Tests

```id="t6k9wr"
python manage.py test
```

---

### 📸 Test Output

A screenshot of test execution is included in:

```id="z2m7kc"
sample_files/test_results.png
```

Example output:

```id="b7x4hn"
Ran 3 tests in 0.45s

OK
```

---

## 📌 Submission Contents

This repository includes:

* ✅ Complete source code
* ✅ Sample CSV input file
* ✅ Sample API response (JSON)
* ✅ Unit test implementation
* ✅ Test execution screenshot
* ✅ Detailed documentation

---

## 👨‍💻 Author

Developed as part of a backend API development assessment using Django REST Framework.

---

## 🏁 Conclusion

This project demonstrates:

* Strong understanding of REST API development
* Clean validation using serializers
* Efficient data processing and optimization
* Robust error handling
* Test-driven development practices

---
