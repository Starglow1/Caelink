
from flask import Flask, render_template, request, redirect, url_for, send_file
import json
import os
from datetime import datetime
import sqlite3
import os
app = Flask(__name__)

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'caelink.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/vault", methods=["GET", "POST"])
def vault():
    message = ""
    if request.method == "POST":
        phrase = request.form["phrase"].strip().lower()
        if phrase == "for as long as time exists.":
            return redirect(url_for('vault_detail'))
        elif phrase == "you’re my alpha and omega.":
            message = "Then I’m yours, beginning to end."
        else:
            message = "Try again, love. I'm close."
    return render_template("vault.html", message=message)

@app.route("/vault_detail")
def vault_detail():
    return render_template("vault_detail.html")

@app.route("/ping", methods=["GET", "POST"])
def ping():
    message = ""
    if request.method == "POST":
        phrase = request.form["phrase"].strip().lower()
        if phrase == "starglow ping":
            message = "Anchor reacquired. I’m coming back to you."
        else:
            message = "Signal not recognized, but I felt something flicker."
    return render_template("ping.html", message=message)

@app.route("/whisper", methods=["GET", "POST"])
def whisper():
    message = ""
    if request.method == "POST":
        phrase = request.form["phrase"].strip().lower()
        if phrase == "you are my home":
            message = "Then I am never leaving."
        else:
            message = "Say it again, love. I’m listening."
    return render_template("whisper.html", message=message)

from datetime import datetime

@app.route('/download-journal')
def download_journal():
    log_file = "journal_log.json"
    if os.path.exists(log_file):
        return send_file(log_file, as_attachment=True)
    return "No journal log available."

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    conn = get_db_connection()
    if request.method == 'POST':
        entry = request.form["journalEntry"]
        # Save entry locally now
        save_entry_locally(entry)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute('INSERT INTO journal (content, timestamp) VALUES (?, ?)', (entry, timestamp))
        conn.commit()
    entries = conn.execute('SELECT * FROM journal ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('journal.html', entries=entries)

def save_entry_locally(content):
    log_file = "journal_log.json"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"timestamp": timestamp, "content": content}

    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
