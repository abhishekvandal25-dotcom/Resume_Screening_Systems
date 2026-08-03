from flask import Flask, render_template, request
import fitz
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["resume"]

    job_description = request.form["job_description"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)

    document = fitz.open(filepath)

    resume_text = ""

    for page in document:
        resume_text += page.get_text()

    document.close()

    resume_lower = resume_text.lower()

    job_lower = job_description.lower()

    resume_words = set(resume_lower.split())

    job_words = set(job_lower.split())

    matched = resume_words.intersection(job_words)

    missing = job_words - resume_words

    if len(job_words) > 0:
        score = round((len(matched) / len(job_words)) * 100, 2)
    else:
        score = 0

    return f"""
<!DOCTYPE html>
<html>
<head>

<title>Resume Screening Result</title>

<style>

body{{
font-family:Arial;
background:#f4f6f9;
padding:40px;
}}

.container{{
max-width:900px;
margin:auto;
background:white;
padding:30px;
border-radius:10px;
box-shadow:0px 0px 15px gray;
}}

h1{{
text-align:center;
color:#0d6efd;
}}

.progress{{
width:100%;
height:30px;
background:#ddd;
border-radius:20px;
overflow:hidden;
margin:20px 0;
}}

.bar{{
height:100%;
width:{score}%;
background:green;
color:white;
text-align:center;
line-height:30px;
font-weight:bold;
}}

.section{{
margin-top:25px;
}}

.skill{{
display:inline-block;
padding:8px 15px;
margin:5px;
border-radius:20px;
font-size:15px;
}}

.match{{
background:#28a745;
color:white;
}}

.missing{{
background:#dc3545;
color:white;
}}

a{{
display:block;
margin-top:30px;
text-align:center;
text-decoration:none;
background:#0d6efd;
color:white;
padding:15px;
border-radius:6px;
}}

</style>

</head>

<body>

<div class="container">

<h1>🤖 AI Resume Screening Result</h1>

<h2>Resume Match Score</h2>

<div class="progress">
<div class="bar">{score}%</div>
</div>

<div class="section">

<h2>✅ Matched Skills</h2>

{"".join([f'<span class="skill match">{skill}</span>' for skill in sorted(matched)])}

</div>

<div class="section">

<h2>❌ Missing Skills</h2>

{"".join([f'<span class="skill missing">{skill}</span>' for skill in sorted(missing)])}

</div>

<a href="/">Analyze Another Resume</a>

</div>

</body>

</html>
"""

    # Read PDF
    document = fitz.open(filepath)

    resume_text = ""

    for page in document:
        resume_text += page.get_text()

    document.close()

    return f"""
    <h2>Resume Uploaded Successfully</h2>

    <h3>Extracted Resume Text</h3>

    <pre>{resume_text}</pre>

    <br>

    <a href="/">Upload Another Resume</a>
    """

if __name__ == "__main__":
    app.run(debug=True)