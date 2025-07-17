# ☁️ OBS File Uploader GUI (Huawei Cloud)

## 📌 Purpose

A desktop GUI tool to upload selected files to Huawei Cloud's OBS (Object Storage Service). Built to simplify the file upload process for non-technical users in operational teams.

---

## 🖼️ GUI Features

✅ Select single or multiple files  
✅ Choose target bucket/folder  
✅ Upload with progress bar  
✅ Logs upload status  
✅ Built with Python GUI (Tkinter / PyQt)

---

## ⚙️ Tech Stack

- Python 3.x  
- `obs-client` (Huawei Cloud SDK)  
- `Tkinter` / `PyQt5`  
- `os`, `shutil`  
- Logging module

---

## 🚀 How to Use

1. Clone the repo  
2. Install dependencies:


4. Select files → Upload → Done!

---

## 🧾 Configuration

Store OBS credentials in `config.ini`:

```ini
[OBS]
access_key=your-access-key
secret_key=your-secret-key
bucket_name=your-bucket
endpoint=obs.region.myhuaweicloud.com
