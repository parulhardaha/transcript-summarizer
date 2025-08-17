from flask import Flask, render_template, request, jsonify
from groq import Groq
import markdown
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key) if groq_api_key else None

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv("EMAIL_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_PASS"),
    MAIL_DEFAULT_SENDER=os.getenv("EMAIL_USER")
)
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_summary():
    summary_html = None
    transcript = ''
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        transcript = file.read().decode("utf-8", errors="ignore")
    else:
        transcript = request.form.get('transcript', '')

    prompt = request.form.get('prompt', '')

    if client is None:
        summary_html = markdown.markdown("**GROQ API key not set.**")
    else:
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a meeting summarizer."},
                    {"role": "user", "content": f"Transcript: {transcript}\nInstruction: {prompt}"}
                ]
            )
            summary_html = markdown.markdown(response.choices[0].message.content)
        except:
            summary_html = markdown.markdown("Error generating summary.")

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({"summary": summary_html})
    return render_template("index.html", summary=summary_html)

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json(silent=True) or request.form
    recipient = data.get('email')
    summary = data.get('summary')
    if not recipient or not summary:
        return jsonify({"error": "email and summary required"}), 400

    try:
        mail.send(Message(subject="Summary", recipients=[recipient], html=summary))
        return jsonify({"status": "sent", "method": "Flask-Mail"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

        

@app.route('/health')
def health():
    k = os.getenv('GROQ_API_KEY')
    return {"groq_key_set": bool(k), "groq_key_masked": f"{k[:4]}...{k[-4:]}" if k and len(k) > 8 else "****"}

@app.route('/test-groq', methods=['GET'])
def test_groq():
    if client is None:
        return jsonify({"ok": False, "error": "GROQ_API_KEY not configured"}), 400
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Tiny health-check assistant."},
                {"role": "user", "content": "Respond with the single word: pong"}
            ],
            max_tokens=5,
            temperature=0
        )
        preview = (getattr(response.choices[0].message, 'content', '') or '').strip()[:200]
        return jsonify({"ok": True, "preview": preview}), 200
    except:
        return jsonify({"ok": False, "error": "Groq API error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
