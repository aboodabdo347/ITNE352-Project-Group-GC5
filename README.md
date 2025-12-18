# ITNE352 Project – Group GC5

**News Service System (Client/Server) using Python, Sockets, JSON, APIs, File I/O**

---

## 👥 Group Information

* **Course Code:** ITNE352 (Network Programming) 
* **Section:** 03
* **Group Name:** GC5

| Student ID | Student Name                    |
| ---------: | ------------------------------- |
|  202204625 | Abdulrahman Abdo Ahmed Shomaila |
|  202208352 | Kadhim Abdulla Kadhim Alhaddar  |

---

## 📅 Semester

**First Semester of 2025–2026** 

---

## Project Title

**News Service System – Client/Server Project**

---

##  📓 Project Description

This project is a **client–server news service system** where:

* The **server** accepts TCP connections (multi-threaded), receives client requests, calls **NewsAPI.org** endpoints, returns results in **JSON**, and saves the full API response into JSON files for evaluation.  
* The **client** connects to the server, shows menus (Headlines / Sources), displays a list of results, then requests **full details** for a selected item.  

✅ Output is limited to **15 results max** (matches `MAX_RESULTS = 15`). 

---

## Table of Contents

1. [Group Information](#group-information)
2. [Semester](#semester)
3. [Project Title](#project-title)
4. [Project Description](#project-description)
5. [File Structure](#file-structure)
6. [Requirements (Setup)](#requirements-setup)
7. [How to Run](#how-to-run)
8. [How to Use the Client Menus](#how-to-use-the-client-menus)
9. [Protocol (Client ↔ Server Messages)](#protocol-client--server-messages)
10. [Scripts Description](#scripts-description)
11. [Additional Concepts Used](#additional-concepts-used)
12. [Acknowledgments](#acknowledgments)
13. [Conclusion](#conclusion)
14. [Resources](#resources)

---

## 📂 File Structure

| File / Folder   | Description                                                             |
| --------------- | ----------------------------------------------------------------------- |
| `server.py`     | Multi-threaded TCP server + NewsAPI requests + validation + JSON saving |
| `client.py`     | Client UI (menus) + sends requests + shows list + requests details      |
| `requirements/` | Dependency files (example: `requirements.txt`)                          |
| `*.json`        | Auto-generated result files: `<client>_<option>_<group_ID>.json`        |
| `.env`          | Contains `API_KEY=...` (not committed)                                  |
| `.gitignore`    | Prevents committing `.env` and generated files                          |

---

## Requirements (Setup)

### 1) Install Python

* Python **3.9+** recommended.



### 2) Install dependencies

Your server uses:

* `requests`
* `python-dotenv`

If you have `requirements/requirements.txt`, install like this:

```bash
pip install -r requirements/requirements.txt
```

Or install manually:

```bash
pip install requests python-dotenv
```

### 3) Add your NewsAPI key

Create a file named `.env` in the project root:

```env
API_KEY=your_newsapi_key_here
```

---

## ▶️ How to Run

### Step 1: Start the server

```bash
python server.py
```

Expected:

```
[YYYY-MM-DD HH:MM:SS] Server started on 127.0.0.1:12345
[YYYY-MM-DD HH:MM:SS] Waiting for client connections...
```

### Step 2: Start the client

```bash
python client.py
```

The client stays connected until you select **Quit**. 

---

## How to Use the Client Menus

According to the project specification, the client has **3 main menus** (Main, Headlines, Sources). 

### Main Menu

* **Search headlines** → opens Headlines menu 
* **List of Sources** → opens Sources menu 
* **Quit** → closes connection 

### Headlines Menu (examples)

* Search for keywords
* Search by category
* Search by country
* List all new headlines
* Back to main menu 

### Sources Menu (examples)

* Search by category
* Search by country
* Search by language
* List all
* Back to main menu 

✅ Allowed parameters:

* Countries: `au, ca, jp, ae, sa, kr, us, ma`
* Languages: `ar, en`
* Categories: `business, general, health, science, sports, technology` 

---

## Protocol (Client ↔ Server Messages)

The server receives **JSON messages** ended by a newline `\n` (it reads until `\n` then parses JSON).

### Message format

```json
{"action": "headlines_keyword", "params": {"q": "bitcoin"}}
```

### Examples (based on your server handlers)

* Headlines list actions start with `headlines_...`
* Sources list actions start with `sources_...`
* Detail requests:

  * `headlines_detail` with `{"index": 1}`
  * `sources_detail` with `{"index": 1}`
* Quit:

```json
{"action":"quit","params":{}}
```

---

## Scripts Description

## server.py

**Purpose:** Multi-threaded news server that handles clients, validates input, fetches NewsAPI data, sends lists/details, and saves JSON files. 

### Used packages

* `socket`, `threading`, `json`, `datetime`, `os`
* `requests`
* `dotenv (python-dotenv)`

### Main classes (from your code)

* **`NewsDataFetcher`**
  Calls NewsAPI endpoints:

  * `top-headlines`
  * `sources`

  Snippet:

  ```python
  api_response = requests.get(endpoint, params=request_params, timeout=10)
  api_response.raise_for_status()
  return api_response.json()
  ```

* **`ParameterValidator`**
  Validates request params (country/language/category/keyword). Uses allowed sets.

* **`ClientConnectionHandler (thread)`**
  Handles each client on a separate thread, logs requests, caches results, supports detail view by index, and saves responses as:

  ```
  <client_name>_<option>_<group_ID>.json
  ```

  (Your code matches this format.) 

  Snippet:

  ```python
  filename = f"{self.username}_{sanitized_action}_{GROUP_IDENTIFIER}.json"
  json.dump(data, file, indent=4)
  ```

* **`NewsServerApplication`**
  Binds to `127.0.0.1:12345`, listens, and accepts clients (at least 3 supported by design). 

---

## client.py

**Purpose:** Connects to server, sends username, shows menus, sends requests, displays lists (max 15), then requests details by index. 

Expected output details:

* Headlines list shows: source name, author, title
* Headlines detail shows: source, author, title, URL, description, publish date/time
* Sources list shows: source name
* Sources detail shows: name, country, description, URL, category, language 

---

## Additional Concepts Used

1. **Multithreading**: each connected client is handled in a separate thread (`ClientConnectionHandler`). 
2. **Object-Oriented Programming (OOP)**: the server design uses multiple classes (`NewsDataFetcher`, `ParameterValidator`, etc.).
3. **Environment variables**: API key is stored in `.env` and loaded using `python-dotenv` (safer than hardcoding).

---

## Acknowledgments

> Not finished yet.
---

## Conclusion

This project implements a complete client/server architecture for a news system using Python sockets, JSON messaging, API integration, multi-threading, and file saving for evaluation, matching the required menus, responses, and output limits.  

---

## Resources

* Python OOP Concepts: [https://www.geeksforgeeks.org/python/python-oops-concepts/](https://www.geeksforgeeks.org/python/python-oops-concepts/)
* Python and REST APIs: [https://realpython.com/api-integration-in-python/](https://realpython.com/api-integration-in-python/)
* NewsAPI: [https://newsapi.org/](https://newsapi.org/)

