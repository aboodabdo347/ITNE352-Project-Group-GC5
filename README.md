# ITNE352-Project-Group-GC5

**Client–Server Application using Python, Sockets, JSON, APIs, and File I/O**

---

## 👥 Team Members

| Student ID | Student Name                    | Group |
| ---------: | ------------------------------- | :---: |
|  202204625 | Abdulrahman Abdo Ahmed Shomaila |  GC5  |
|  202208352 | Kadhim Abdulla Kadhim Alhaddar  |  GC5  |

---
## Project Overview

This project is a **client–server news system** built in Python.

* The **server** handles multiple clients, fetches data, and sends results as JSON.
* The **client** connects to the server, sends requests, and displays the news headlines or sources.

---

## 📂 Files

| File                       | Description                                                          |
| -------------------------- | -------------------------------------------------------------------- |
| `server.py`                | Runs the server and handles client connections.                      |
| `client.py`                | Connects to the server and interacts with the user.                  |
| `*.json`                   | Generated automatically by the server to save each client’s results. |
| `.gitignore` | Prevents sensitive files (like `.env` with API keys). |
---

## Requirements

Make sure you have installed:

```bash
Python 3.9 or newer
```

No extra libraries till now.

---

## ▶️ How to Run the Application

### 1. Start the Server

Open **Terminal 1** and run:

```bash
python server.py
```

You should see:

```
Server listening on 127.0.0.1:5000
```

### 2. Start the Client

Open **Terminal 2** and run:

```bash
python client.py
```

Then:

* Enter your name.
* Type a **keyword** (e.g., `sports`, `python`) to get fake news.
* Type **quit** to exit.

### 3. Output Files

After running, the server will create a file like:

```
user_demo.json
```

that stores the results for each user.
