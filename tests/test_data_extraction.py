import pytest
from io import BytesIO
from reportlab.pdfgen import canvas
from src.req import extract_incident_data

@pytest.fixture
def sample_pdf():
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer)
    c.drawString(100, 800, "NORMAN POLICE DEPARTMENT")
    c.drawString(100, 780, "Date / Time          Incident Number   Location           Nature            Incident ORI")
    c.drawString(100, 760, "2024-01-01 12:00     12345            Main St            Theft             OK123")
    c.drawString(100, 740, "2024-01-02 14:30     67890            Elm St             Assault           OK456")
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer

def test_extract_incident_data(sample_pdf):
    incidents = extract_incident_data(sample_pdf)
    assert len(incidents) == 2
    assert incidents[0]['date_time'] == "2024-01-01 12:00"
    assert incidents[0]['nature'] == "Theft"
    assert incidents[1]['incident_ori'] == "OK456"
