from flask import Flask, render_template
import os, sqlite3, shutil

app = Flask(__name__)

def export_chrome_history():
    """
    Reads Chrome's local browsing history and writes it to data.txt.
    Works on Windows.
    """
    history_path = os.path.expanduser(
        r"~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"
    )

    if not os.path.exists(history_path):
        print("⚠️ Chrome history file not found.")
        return 0

    temp_db = "History_temp"
    shutil.copy2(history_path, temp_db)

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT url, title, last_visit_time
    FROM urls
    ORDER BY last_visit_time DESC
    LIMIT 500
    """)
    rows = cursor.fetchall()
    conn.close()

    with open("data.txt", "w", encoding="utf-8") as f:
        for url, title, _ in rows:
            title = title or "No title"
            f.write(f"{title} - {url}\n")

    print(f"✅ Exported {len(rows)} history items to data.txt")
    return len(rows)

@app.route("/")
def index():
    # Automatically export when page opens
    count = export_chrome_history()
    return render_template("index.html", count=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
