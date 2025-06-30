
# FundGuard – Government Tender Risk Analyzer
A visually appealing web app to detect corruption in government tenders.
A data-driven platform that detects corruption patterns in government tender allocations using CSV data and visual analytics.

# 🚨 FundGuard – Government Tender Risk Analyzer

**FundGuard** is an AI-assisted web application that analyzes government tender data for red flags such as over-budget spending, vendor repetition, and suspicious clauses. It ensures transparency and helps identify potential fraud in public procurement.


## 🔍 Key Features

 HEAD
#  FEATURES 
  - Upload and analyze CSV files containing tender data
- Automatic risk flagging for:
  - Over-budget tenders (Final Cost > 1.5 × Estimated Cost)
  - Repeated vendor allocations (same vendor winning > 3 tenders)
- Interactive dashboard with:
  - Total tenders count
  - Flagged tenders count
  - Risk distribution pie chart
- Downloadable report of flagged tenders
- Responsive data table with all tender details
  
 # Tech Stack
   * Frontend: HTML5, Bootstrap 5, Chart.js
   * Backend: Python Flask
   * Data Processing: Pandas
   * Deployment Ready: Easily deployable on platforms like Heroku or Render
     
# Installation & Usage
🧰 Setup Instructions
1. Clone the repository:
 
``` git clone https://github.com/Gargibajpai/FundGuard.git```

```cd FundGuard```

3. (Optional) Create and activate a virtual environment:
# Windows
```python -m venv venv```

```venv\Scripts\activate```

# macOS/Linux
```python3 -m venv venv```

```source venv/bin/activate```

3. Install dependencies:
   
  ```pip install -r requirements.txt```

5. Run the app:
   
  ```python app.py```

7. Visit: ```http://127.0.0.1:5000```
   

9. 🔐 Login Details
Use these credentials to log in:

Username: admin

Password: admin123



## 📸 Demo Screenshot

Here’s a preview of the FundGuard dashboard in action:
![image](https://github.com/user-attachments/assets/aa721db2-ce6b-4a6f-825f-d663e18e40e3)
![image](https://github.com/user-attachments/assets/2594b9ab-0bec-4b59-8b5e-25f336158c87)
![image](https://github.com/user-attachments/assets/98ee8c16-8d5e-4d42-ba4f-6500b0976759)
![image](https://github.com/user-attachments/assets/412b2fb3-5fd9-4ee9-ae0d-b0efecfa91b5)
![image](https://github.com/user-attachments/assets/ba916147-982e-4c4f-afc5-cfcd7c0e7a87)


![image](https://github.com/user-attachments/assets/192c27f9-c6df-482f-b363-b71c4375d022)

- 📁 **CSV Upload**: Upload tender files for instant audit  
- 🧠 **Risk Scoring Engine**: AI-based fraud risk score (0–100)  
- 📄 **NLP Clause Analyzer**: Detect unfair or suspicious clauses  
- 💬 **FundBot Chatbot**: Ask questions on tenders or fraud flags  
- 📊 **Interactive Dashboard**: View flagged entries and stats  
- 🌙 **Dark Mode**: Persistent theme switcher  
- ⬇️ **Export**: Download flagged data as CSV  
- 🔐 **Secure Login**: Session-based access control  

---

## 🛠️ Tech Stack

| Layer        | Technology              |
|--------------|-------------------------|
| Frontend     | HTML, CSS, Bootstrap 5  |
| Backend      | Python, Flask           |
| Visualization| Chart.js                |
| AI/NLP Logic | Pandas, OpenAI API      |
| Chatbot      | Vanilla JS + Flask API  |

---

## 📦 Project Structure

```

FundGuard/
│
├── static/
│   ├── style.css           # Theme & layout styling
│   ├── logo.png            # Navbar/login logo
│   └── illustration.png    # Landing hero image
│
├── templates/
│   ├── home.html           # Landing page
│   ├── login.html          # Login + chatbot
│   └── dashboard.html      # Analysis dashboard
│
├── uploads/                # Uploaded/flagged CSVs
│
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies
└── README.md               # Project overview

````

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/<your-username>/FundGuard.git
cd FundGuard
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
````

🔗 Open in browser: `http://127.0.0.1:5000/`

---

## 📊 Sample CSV Format

```
Tender ID,Department,Estimated Cost,Final Cost,Vendor
T1234,Health,1000000,1800000,ABC Corp
T5678,Transport,800000,750000,XYZ Ltd
T9101,Education,600000,1200000,ABC Corp
```

✅ AI will auto-flag:

* ⚠ Over Budget (≥ 1.5× estimate)
* 🔁 Vendor Repeat (more than 3 entries)
* 📌 Duplicate Invoices
* 💬 Suspicious Descriptions
* 📅 Weekend Approvals

---

## 🧠 FundBot (Chat Assistant)

A chatbot is embedded on the login page. Ask:

* “How does FundGuard detect fraud?”
* “What does risk score 75 mean?”
* “What flags are shown for tender repeats?”

Works offline with logic-based fallback if OpenAI is unavailable.

---

## 🔐 Default Login Credentials

```bash
Username: admin
Password: admin123
```

(You can change these in `app.py`)

---

## 📤 Export Results

After uploading and auditing, go to the dashboard → Click ⬇ Download CSV to export all flagged tender rows.

---

## ✨ Future Scope

* 🔐 Multi-user login with role-based access
* 📚 NLP-based full tender clause auditing
* 🧠 Fine-tuned ML model for fraud patterns
* ☁️ Cloud CSV storage with analytics

---

## 👥 Team Members
* **Gargi Bajpai**
  [GitHub →](https://github.com/Gargibajpai)

* **Ashmita Goyal**
  [GitHub →](https://github.com/ashmita1206)

* **Lipika Tomar**
  [GitHub →](https://github.com/LipikaTomar)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

