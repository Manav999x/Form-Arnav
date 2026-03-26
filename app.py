from flask import Flask, render_template, request
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

app = Flask(__name__)

PDF_FOLDER = "/tmp/generated_pdfs"
os.makedirs(PDF_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form

    file_name = f"{data['team'].replace(' ', '_')}.pdf"
    file_path = os.path.join(PDF_FOLDER, file_name)

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("ARNAV FOUNDATION", styles['Title']))
    content.append(Paragraph("Summer Cricket Tournament 2026", styles['Heading2']))
    content.append(Spacer(1, 10))

    # Team Info
    content.append(Paragraph(f"<b>Team Name:</b> {data['team']}", styles['Normal']))
    content.append(Paragraph(f"<b>Contact Person:</b> {data['contact']}", styles['Normal']))
    content.append(Paragraph(f"<b>Phone Number:</b> {data['phone']}", styles['Normal']))
    content.append(Spacer(1, 10))

    # Players
    content.append(Paragraph("<b>Players:</b>", styles['Heading3']))

    for i in range(1, 8):
        player = data.get(f"p{i}", "")
        if player:
            content.append(Paragraph(f"Player {i}: {player}", styles['Normal']))

    content.append(Spacer(1, 20))

    # Declaration
    content.append(Paragraph(
        "We declare that all information provided is correct and we agree to tournament rules.",
        styles['Normal']
    ))

    doc.build(content)

    return f"""
    <h2>✅ PDF Generated Successfully!</h2>
    <p>Saved in: generated_pdfs/{file_name}</p>
    <a href="/">Go Back</a>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
