from flask import Flask, render_template, request, make_response
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table,  TableStyle, Image, Spacer, Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_RIGHT
from io import BytesIO

app = Flask(__name__)

# HTML form template
@app.route('/')
def index():
    return render_template('form.html')

# Handle form submission
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Get user details from the form
    user_name = request.form['name']
    labrefno = request.form['labrefno']
    client_ref_no = request.form['client_ref_no']
    concern = request.form['concern']
    date = request.form['date']
    invoiceno = request.form['invoiceno']
    
    # Get description details
    # Get description details
    descriptions = request.form.getlist('description[]')
    qtys = request.form.getlist('qty[]')
    rates = request.form.getlist('rate[]')

    # Calculate amounts and convert to float
    amounts = [float(qty) * float(rate) for qty, rate in zip(qtys, rates)]
    discount = float(request.form['discount'])

    # Calculate total amount
    total_amount = sum(amounts)
    grand_total=total_amount-discount


    # Generate PDF
    pdf_buffer = generate_pdf_document(user_name, labrefno,client_ref_no,concern,date, descriptions, qtys, rates, amounts,total_amount,discount,grand_total,invoiceno)
    
    # Serve PDF to user for download
    filename = f"{user_name}_{date}_tax_invoice.pdf"
    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    response.headers['Content-type'] = 'application/pdf'
    
    return response

# Generate PDF document
# Generate PDF document
# Generate PDF document
# Generate PDF document
def generate_pdf_document(user_name, labrefno, client_ref_no, concern, date, descriptions, qtys, rates, amounts, total_amount, discount, grand_total,invoiceno):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    p_date_style = styles["Normal"]
    p_date_style.alignment = 2  # Right alignment

    # Construct content
    content = []

    # Load image
    image_path = "uploads/taxinvoice.PNG"
    image = Image(image_path, width=450, height=100)
    
    # Add image to content
    content.append(image)
    content.append(Spacer(1, 12))

    # Proforma Invoice
    styles["Heading3"].alignment = TA_RIGHT

# Append the paragraph with the adjusted style
    content.append(Paragraph("<b>Proforma Invoice</b>", styles["Heading3"]))
    content.append(Spacer(1, 12))

    # Customer Details
    content.append(Paragraph(f"<b>Customer Details:</b> {user_name}"))
    content.append(Spacer(1, 12))


   

    # Table
    table_data = [
    ["Lab Ref No:", labrefno, "Invoice No:", invoiceno],
    ["Client Ref No:", client_ref_no, "Date:", date],
    [f"Concern: {concern}", "", "", ""],  # Adjusted the format for the Concern row
    ["Item No", "Description", "Qty", "Rate (Rs.)", "Amount (Rs.)"]
]
    for i, (description, qty, rate, amount) in enumerate(zip(descriptions, qtys, rates, amounts), start=1):
        table_data.append([i, description, qty, rate, amount])

    table_data.extend([
        ["", "", "", "Sub Total (LKR)", total_amount],
        ["", "", "", "Discount Total (LKR)", discount],
        ["", "", "", "Grand Total (LKR)", grand_total]
    ])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 2), colors.white),
        ('BACKGROUND', (0, 3), (-1, 3), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 4), 'Helvetica-Bold'),
        ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('SPAN', (0, 2), (2, 2)),
    ]))

    content.append(table)
    content.append(Spacer(1, 12))

    # Additional text
    # Additional text
    # Additional text
    additional_text = [
    "Cheques should be in favor of Enviroequip (PVT) LTD & crossed account payee only.",
    "Our bank details are as follows:",
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b><div style='text-align: center;'>Hatton National Bank PLC (Code – 7083)</div></b>",
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b><div style='text-align: center;'>Mirihana Branch (Code – 204)</div></b>",
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b><div style='text-align: center;'>A/C No. 204010000927</div></b>",
    "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b><div style='text-align: center;'>Account Name – Enviroequip (PVT) LTD</div></b>",
    "Please mention your invoice number(s) in remarks."
    ]

    for text in additional_text:
        content.append(Paragraph(text))
        content.append(Spacer(1, 20))


    content.append(Spacer(1, 12))

    # Signature text with tabs
    signature_text = [
        "Prepared by",
        "Certified by",
        "Customer’s Signature"
    ]

    # Generate signature block with dotted lines and text on separate lines
 # Generate signature block with dotted lines and text on separate lines
    signature_div = f"""
    <div style="display: flex; justify-content: space-between;">
        <div style="width: 33%; text-align: left;">{'.' * 50}</div>
        <div style="width: 33%; text-align: center;">{'.' * 50}</div>
        <div style="width: 33%; text-align: right;">{'.' * 50}</div>
    </div>
    <div style="display: flex;">
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<div style="width: 33%; text-align: left;">{signature_text[0]}</div>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<div style="width: 33%; text-align: center;">{signature_text[1]}</div>
   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <div style="width: 33%; text-align: right;">{signature_text[2]}</div>
    </div>
    """

    # Append the signature_div to the content
    content.append(Paragraph(signature_div))







    # Build PDF
    doc.build(content)

    return pdf_buffer

    
if __name__ == '__main__':
    app.run(debug=True)
