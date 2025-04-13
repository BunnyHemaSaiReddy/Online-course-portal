import io
import tempfile
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
def create_certificate(name, date):
    overlay_stream = io.BytesIO()
    can = canvas.Canvas(overlay_stream, pagesize=landscape(letter))
    can.setFont("Helvetica-Bold", 24)
    can.drawCentredString(415, 330, name)
    can.setFont("Helvetica", 16)
    can.drawCentredString(415, 300, f"Date: {date}")
    can.save()
    overlay_stream.seek(0)

    template = PdfReader("online_course/certificate_template.pdf")
    overlay = PdfReader(overlay_stream)
    output = PdfWriter()
    
    base_page = template.pages[0]
    base_page.merge_page(overlay.pages[0])
    output.add_page(base_page)

    output_stream = io.BytesIO()
    output.write(output_stream)
    output_stream.seek(0)
    
    return output_stream

# create_certificate_bytes("name", "date")