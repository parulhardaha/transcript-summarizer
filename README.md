# Transcript Summarizer

Simple Flask app that sends transcripts to Groq for summarization and allows emailing the result.

Setup

1. Create and activate a venv:

```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file (copy `.env.example`) and set `GROQ_API_KEY`, `EMAIL_USER`, and `EMAIL_PASS`.

4. Run the app:

```powershell
$env:FLASK_APP = "app.py"
flask run --debug
```

Notes

- Do not commit `.env` or any secrets. Rotate exposed keys immediately.
- The app includes a `/health` endpoint that reports whether `GROQ_API_KEY` is set.
