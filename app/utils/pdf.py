from reportlab.lib import colors
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)


def generate_invoice(
    freelancer, client, client_address, project_name, project_description,
    invoice_date, invoice_number, status, total_amount,
):
    """
    Generate a PDF invoice.

        This function creates a PDF invoice document using the provided
        details about the freelancer, client, project, and invoice
        information. The generated PDF includes sections for freelancer
        and client details, project description, invoice metadata, and
        payment methods.

        Args:
            freelancer (str): The name of the freelancer issuing the invoice.
            client (str): The name of the client receiving the invoice.
            client_address (str): The address of the client.
            project_name (str): The name of the project for which the
                                invoice is issued.
            project_description (str): A brief description of the project.
            invoice_date (str): The date the invoice is issued.
            invoice_number (str): A unique identifier for the invoice.
            status (str): The status of the invoice (e.g., "Paid", "Unpaid").
            total_amount (float): The total amount to be paid for the project.

        Returns:
            bytes: The binary content of the generated PDF invoice.

        Notes:
            - The function uses the `reportlab` library to generate the PDF.
            - The invoice includes a table summarizing the project details
              and total amount.
            - Payment methods are hardcoded as placeholders and should be
              updated as needed.
            - Future enhancements may include tax calculations or additional
              styling.

        Raises:
            ValueError: If any required argument is missing or invalid.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(filename=buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("<b>INVOICE</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Freelancer Information
    elements.append(Paragraph(f"<b>Freelancer:</b> {freelancer}",
                              styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Client Information
    elements.append(Paragraph(f"<b>Client:</b> {client}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Address:</b> {client_address}",
                              styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Project Details
    elements.append(Paragraph(
        f"<b>Project:</b> {project_name}", styles["Normal"]))
    elements.append(Paragraph(
        f"<b>Description:</b> {project_description}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Invoice Info
    elements.append(Paragraph(f"<b>Invoice Date:</b> {invoice_date}",
                              styles["Normal"]))
    elements.append(Paragraph(f"<b>Invoice Number:</b> {invoice_number}",
                              styles["Normal"]))
    elements.append(Paragraph(f"<b>Status:</b> {status}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Invoice Items Table
    data = [["Project", "Description", "Total Amount"]]
    data.append([project_name, project_description, f"${total_amount:.2f}"])

    # FUTURE: Add the tax calculation here

    # Total Row
    data.append(["", "", "<b>Total:</b>", f"<b>${total_amount:.2f}</b>"])

    # Table Styling
    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (-2, -1), (-1, -1), "Helvetica-Bold"),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Payment Section
    elements.append(Paragraph("<b>Payment Methods:</b>", styles["Heading3"]))
    elements.append(Paragraph(
        "• PayPal: paypal.me/yourname", styles["Normal"]))
    elements.append(Paragraph("• Stripe: stripe.com/pay/yourname",
                              styles["Normal"]))
    elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
