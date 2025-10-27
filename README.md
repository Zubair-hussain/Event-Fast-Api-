---

# HasData SERP FastAPI Backend

## Intelligent Search API with Automatic Location Detection

This repository hosts a **FastAPI backend** that fetches **localized Google Search (SERP) data** using the [HasData API](https://hasdata.com/).
It automatically detects the **user’s city, region, and country** from their IP address — making it ideal for **Streamlit**, **React**, or **mobile apps** that need real-time, location-based search results.

---

## Overview

This backend serves as a bridge between your frontend application and the HasData Google SERP API.

* Automatically detects user location from IP
* Fetches local Google search results (e.g., events, exhibitions, services)
* Built using FastAPI for speed and scalability
* Can be deployed directly on **Streamlit Cloud** or any server that supports Python
* Requires a HasData API key (you can update it manually in the code)

---

## Project Structure

```
hasdata-serp-api/
│
├── main.py              # FastAPI app entry point
├── fetch_serp.py        # Handles HasData API requests and location detection
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

---

## How It Works

1. The client (Streamlit app or web app) sends a POST request to `/serp`:

   ```json
   {
     "query": "Exhibition"
   }
   ```

2. The backend:

   * Detects the user’s location from their IP (using `ipapi.co`, fallback `ipinfo.io`)
   * Sends a request to HasData’s Google SERP API with that location
   * Returns structured JSON data to the client

3. Example Response:

   ```json
   {
     "detected_location": "Karachi,Sindh,Pakistan",
     "results": {
       "local_results": [...],
       "search_metadata": {...}
     }
   }
   ```

---

## API Endpoint

### POST `/serp`

**Request Body:**

```json
{
  "query": "Digital Marketing",
  "location": "optional, auto-detected if empty"
}
```

**Response:**

```json
{
  "detected_location": "Lahore,Punjab,Pakistan",
  "results": {...}
}
```

**Parameters:**

| Field         | Type   | Default       | Description              |
| ------------- | ------ | ------------- | ------------------------ |
| `query`       | string | required      | Your search term         |
| `location`    | string | auto-detected | User location (optional) |
| `gl`          | string | "pk"          | Country code             |
| `device_type` | string | "desktop"     | Device type              |
| `tbs`         | string | "qdr:w"       | Time-based search filter |
| `tbm`         | string | "lcl"         | Search type (local)      |
| `num`         | int    | 50            | Number of results        |

---

## Setup Instructions

### 1. Update Your HasData API Key

In `fetch_serp.py`, replace this placeholder with your real key:

```python
API_KEY = "your_actual_api_key_here"
```

*(You are not required to use `.env` — keys are hardcoded for now.)*

---

### 2. Install Dependencies (Optional for Local Testing)

If testing locally:

```bash
pip install -r requirements.txt
```

---

### 3. Run Locally (Optional)

```bash
uvicorn main:app --reload
```

Open your browser at:

```
http://127.0.0.1:8000/docs
```

---

## Streamlit Cloud Deployment Guide

Follow these steps to deploy the FastAPI backend on **Streamlit Cloud** (or similar platforms):

### Step 1. Push the Repo to GitHub

Commit and push all files, including:

```
main.py
fetch_serp.py
requirements.txt
README.md
```

---

### Step 2. Go to Streamlit Cloud

* Visit [https://share.streamlit.io](https://share.streamlit.io)
* Click **“New App”**
* Connect your GitHub repository

---

### Step 3. Configure Repository

* Select the branch (e.g., `main`)
* In the **Main file path**, enter:

  ```
  main.py
  ```
* Streamlit will automatically detect dependencies from `requirements.txt`

---

### Step 4. Dependencies (requirements.txt)

```
fastapi
requests
```

**Note:**
You do not need to include `uvicorn` because Streamlit manages the execution environment automatically.

---

### Step 5. Deploy

* Click **“Deploy”**
* Wait for build and deployment to complete
* Streamlit will host your FastAPI backend automatically

---

## Location Detection Logic

| Priority | API Service                     | HTTPS | API Key                | Limit     | Purpose        |
| -------- | ------------------------------- | ----- | ---------------------- | --------- | -------------- |
| 1        | [ipapi.co](https://ipapi.co/)   | Yes   | None                   | 30K/month | Primary source |
| 2        | [ipinfo.io](https://ipinfo.io/) | Yes   | None (for light usage) | ~1K/day   | Backup source  |

If both fail, it defaults to `Karachi,Sindh,Pakistan`.

---

## Example Frontend Integration

You can call this API directly from any frontend:

```javascript
const response = await fetch("https://your-streamlit-app.streamlit.app/serp", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ query: "Exhibition near me" })
});

const data = await response.json();
console.log(data.detected_location, data.results);
```

---

## License

This project is open for educational or internal business use.
All API data is retrieved from [HasData](https://hasdata.com/) according to their terms and policies.

---

## Author

**Developed by:** Zubair Hussain, Mudasir Malik, Abdul Mutaal Khan 
**Purpose:** To create a simple and reliable backend for HasData’s API with automatic user location detection.
**Tech Stack:** FastAPI, Python, HasData API, IP geolocation (ipapi.co + ipinfo.io)

---


