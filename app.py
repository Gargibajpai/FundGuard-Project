import os
import re
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Setup (Optional)
client = None
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_api_key)
        print("✅ OpenAI Connected")
    except Exception as e:
        print("❌ OpenAI Import Error:", e)

# Flask Setup
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallbacksecretkey")

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'csv'}

USERNAME = 'admin'
PASSWORD = 'admin123'

# --- Helpers ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def flag_issue(df, index, issue):
    current = df.at[index, 'Issues']
    df.at[index, 'Issues'] = current + (' | ' if current else '') + issue
    df.at[index, 'Status'] = '🚩 Attention Needed'

def run_ai_audit(df):
    df['Status'] = '✅ OK'
    df['Issues'] = ''

    # Over Budget
    for i in df.index:
        if df.at[i, 'Final Cost'] > 1.5 * df.at[i, 'Estimated Cost']:
            flag_issue(df, i, '⚠ Over Budget')

    # Vendor Repeat
    df['Vendor Count'] = df.groupby('Vendor')['Vendor'].transform('count')
    for i in df.index:
        if df.at[i, 'Vendor Count'] > 3:
            flag_issue(df, i, '🔁 Vendor Repeat')
    df.drop('Vendor Count', axis=1, inplace=True)

    # Duplicate Invoice
    if 'Invoice No' in df.columns:
        dupes = df['Invoice No'].duplicated(keep=False)
        for i in df[dupes].index:
            flag_issue(df, i, '📌 Duplicate Invoice')

    # Weekend Approval
    if 'Approval Date' in df.columns:
        df['Approval Date'] = pd.to_datetime(df['Approval Date'], errors='coerce')
        for i in df.index:
            if pd.notnull(df.at[i, 'Approval Date']) and df.at[i, 'Approval Date'].weekday() >= 5:
                flag_issue(df, i, '📅 Weekend Approval')

    # Future Tender Date
    if 'Tender Date' in df.columns:
        df['Tender Date'] = pd.to_datetime(df['Tender Date'], errors='coerce')
        today = pd.Timestamp.today()
        for i in df.index:
            if pd.notnull(df.at[i, 'Tender Date']) and df.at[i, 'Tender Date'] > today:
                flag_issue(df, i, '⏳ Future Tender Date')

    # Suspicious Keywords
    suspicious_keywords = ['bribe', 'kickback', 'illegal', 'falsified', 'ghost vendor']
    if 'Tender Description' in df.columns:
        for i in df.index:
            text = str(df.at[i, 'Tender Description']).lower()
            if any(word in text for word in suspicious_keywords):
                flag_issue(df, i, '💬 Suspicious Description')

    return df

# --- Routes ---
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('upload'))
        else:
            return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('upload.html')  # separate upload page

    file = request.files.get('file')
    if not file or file.filename == '' or not allowed_file(file.filename):
        return 'Invalid file type', 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    df = pd.read_csv(filepath)
    df = run_ai_audit(df)

    flagged_path = os.path.join(UPLOAD_FOLDER, 'flagged.csv')
    df.to_csv(flagged_path, index=False)

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    flagged_path = os.path.join(UPLOAD_FOLDER, 'flagged.csv')
    data, summary = [], {}

    if os.path.exists(flagged_path):
        df = pd.read_csv(flagged_path)
        data = df.to_dict(orient='records')
        summary = {
            'total': len(df),
            'flagged': len(df[df['Status'] != '✅ OK']),
            'ok': len(df[df['Status'] == '✅ OK']),
            'issues': len(df[df['Status'] == '🚩 Attention Needed']),
            'over': len(df[df['Issues'].str.contains('Over Budget', na=False)]),
            'repeat': len(df[df['Issues'].str.contains('Vendor Repeat', na=False)])
        }

    return render_template('dashboard.html', data=data, summary=summary)

@app.route('/export')
def export():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    flagged_path = os.path.join(UPLOAD_FOLDER, 'flagged.csv')
    return send_file(flagged_path, as_attachment=True) if os.path.exists(flagged_path) else ("No file to export", 404)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# --- AI APIs ---
@app.route('/api/risk_score', methods=['POST'])
def risk_score():
    text = request.json.get('text', '').lower()
    if not text:
        return jsonify({'risk_score': "Error", 'error': "Empty input"})

    # Rule-based prototype scoring
    if "bribe" in text or "kickback" in text or "ghost vendor" in text:
        return jsonify({'risk_score': "95 / 100", 'source': 'Prototype'})
    elif "falsifying" in text or "fake invoice" in text or "fraud" in text:
        return jsonify({'risk_score': "90 / 100", 'source': 'Prototype'})
    elif "single vendor" in text or "no bidding" in text:
        return jsonify({'risk_score': "85 / 100", 'source': 'Prototype'})
    elif "urgency" in text:
        return jsonify({'risk_score': "70 / 100", 'source': 'Prototype'})
    elif "open tender" in text or "transparent bidding" in text:
        return jsonify({'risk_score': "20 / 100", 'source': 'Prototype'})
    else:
        return jsonify({'risk_score': "40 / 100", 'source': 'Prototype (default)'})

@app.route('/api/nlp_clause', methods=['POST'])
def nlp_clause():
    clause = request.json.get('clause', '').lower()
    if not clause:
        return jsonify({'reply': "⚠ No clause provided."})

    if "without bidding" in clause or "no competition" in clause:
        return jsonify({'reply': "⚠ Suspicious clause: Award without open competition."})
    elif "pre-approved vendor" in clause or "only selected vendors" in clause:
        return jsonify({'reply': "⚠ Restricted clause: Limited vendor participation."})
    elif "open tender" in clause or "transparent bidding" in clause:
        return jsonify({'reply': "✅ Fair clause: Encourages transparency."})
    elif "retrospective approval" in clause:
        return jsonify({'reply': "⚠ Red flag: Clause allows post-event approvals."})
    elif "urgent procurement" in clause:
        return jsonify({'reply': "⚠ May bypass standard checks under urgency."})
    else:
        return jsonify({'reply': "📝 Clause reviewed: No major red flags detected."})

@app.route('/api/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt', '').lower()

    if not prompt:
        return jsonify({"reply": "⚠ Please enter a question."})

    if "upload" in prompt:
        return jsonify({"reply": "📁 You can upload your CSV file from the Upload tab."})
    elif "risk score" in prompt:
        return jsonify({"reply": "🧠 Risk score is calculated based on cost anomalies, vendor patterns, and suspicious language."})
    elif "flag" in prompt or "issue" in prompt:
        return jsonify({"reply": "🚩 Tenders are flagged for issues like over-budget, vendor repetition, and weekends approvals."})
    elif "contact" in prompt or "support" in prompt:
        return jsonify({"reply": "📞 Contact support at help@fundguard.ai for queries."})
    else:
        return jsonify({"reply": "🤖 I’m FundBot! Ask me about tenders, clauses, uploads, or AI audit rules."})

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)
