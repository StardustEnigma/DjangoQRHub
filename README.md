﻿# DjangoQRHub
# ⛽ Petrol Pump Payments – QR Code Generator & Scanner

A modern Django web application to **generate and manage QR codes** for petrol pump payments. This project simplifies customer identification using QR codes embedded with data and mobile numbers, making transaction processes faster and more secure.

---

## 🚀 Features

- ✅ Generate QR codes based on customer mobile number and additional data
- ✅ Store generated QR codes in the database
- ✅ Auto-save QR codes as images in the `media/qr_codes` directory
- ✅ Download QR image feature
- ✅ Basic QR scan page setup (future-ready for camera integration)
- ✅ Tailwind CSS for responsive and aesthetic UI
- ✅ Input validation and clean error handling

---

## 📸 Demo Screenshots

| Generate QR | QR Output |
|-------------|-----------|
| ![Generate](media/demo/generate_qr.png) | ![QR](media/demo/generated_qr.png) |

---
## 🛠 Tech Stack

- **Backend:** Django 5.x (Python)
- **Frontend:** Tailwind CSS
- **Database:** SQLite
- **QR Generation:** `qrcode` Python library
- **Storage:** Django FileSystemStorage
- **UI:** Responsive design for both desktop and mobile

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/DjangoQRHub.git
cd DjangoQRHub
```
### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate       # On Windows
source .venv/bin/activate    # On macOS/Linux
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```
### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
### 5. Start the server
```bash
python manage.py runserver
Visit: http://127.0.0.1:8000/
```

## 🧪 Usage
 ### 🔹 Generate QR
- Go to Generate QR tab.

- Enter a valid 10-digit mobile number.

- Enter text to embed into the QR (like name, pump ID, etc.).

- Submit the form.

- QR code will be generated, displayed, and available for download.

### 🔹 Scan QR
-  Go to the Scan QR tab.

- You will see a prepared UI with placeholder for QR scanning.

- This view is ready to be integrated with a webcam scanner using JavaScript or QR decoding libraries like pyzbar or opencv.

## 🙋‍♂️ Author
### Atharva Mandle
### 🎓 B.Tech CSE @ RBU Nagpur
### 📧 atharvamandle19@gmail.com
### 🔗 LinkedIn
