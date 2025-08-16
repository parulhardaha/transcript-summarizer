from flask import Flask, render_template, request
from groq import Groq
import markdown
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['phardaha5@gmail.com'] = os.getenv("EMAIL_USER")  
app.config['nothing'] = os.getenv("EMAIL_PASS")  
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_summary():
    summary_html = None

    # Get transcript file
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        try: 
            transcript = file.read().decode("utf-8", errors="ignore")
        except Exception as e: 
            return render_template("index.html", summary=f"Error reading file: {str(e)}")
    else:
        transcript = request.form.get('transcript', '')  # text input

    prompt = request.form.get('prompt', '')

    #Call Groq API
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a meeting summarizer."},
                {"role": "user", "content": f"Transcript: {transcript}\nInstruction: {prompt}"}
            ]
        )
        summary = response.choices[0].message.content
        summary_html = markdown.markdown(summary)  # covert to HTML here too
    except Exception as e:
        summary_html = markdown.markdown(f"Error generating summary: {str(e)}")

    return render_template("index.html", summary=summary_html)

if __name__ == "__main__":
    app.run(debug=True)
