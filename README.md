# 📝 AetherNotes - Note Taking App

Aplikasi **Note Taking** berbasis **Client-Server** yang dikembangkan sebagai tugas akhir mata kuliah **Client-Server Programming**. Aplikasi ini menggunakan **Python Flask** sebagai backend, **SQLite** sebagai database, dan **HTML** sebagai antarmuka pengguna.

---

## ✨ Fitur

* ➕ Tambah catatan
* 📄 Lihat daftar catatan
* ✏️ Edit catatan
* 🗑️ Hapus catatan
* 📂 Arsip catatan
* 📌 Pin catatan

---

## 🛠 Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML
* **Database:** SQLite
* **Protocol:** HTTP (REST API)

---

## 📂 Struktur Project

```text
NoteTakingApp/
│
├── app.py
├── notes.db
├── templates/
│   └── index.html
├── requirements.txt
└── README.md
```

---

## 📋 Prasyarat

Pastikan sudah menginstal:

* Python 3
* Flask

Install Flask:

```bash
pip install flask
```

---

## ▶️ Cara Menjalankan

1. Clone repository

```bash
git clone https://github.com/username/NoteTakingApp.git
```

2. Masuk ke folder project

```bash
cd NoteTakingApp
```

3. Jalankan aplikasi

```bash
python app.py
```

4. Buka browser

```text
http://127.0.0.1:5000
```

---

## 🌐 Endpoint API

| Method | Endpoint              | Fungsi                    |
| ------ | --------------------- | ------------------------- |
| GET    | `/api/notes`          | Menampilkan semua catatan |
| GET    | `/api/notes/archived` | Menampilkan catatan arsip |
| POST   | `/api/notes`          | Menambah catatan          |
| PUT    | `/api/notes/<id>`     | Mengubah catatan          |
| DELETE | `/api/notes/<id>`     | Menghapus catatan         |

---

## 🔄 Arsitektur Sistem

```text
Browser (Client)
       │
    HTTP Request
       │
Flask Server
       │
    SQLite Database
```

---


## 📚 Referensi

* Flask Documentation: https://flask.palletsprojects.com/
* SQLite Documentation: https://www.sqlite.org/

