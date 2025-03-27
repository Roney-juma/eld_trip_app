from reportlab.pdfgen import canvas

def generate_log_pdf(trip_data, output_path):
    c = canvas.Canvas(output_path)
    c.drawString(100, 750, f"Trip Log: {trip_data['current_location']} → {trip_data['dropoff_location']}")
    c.drawString(100, 730, f"Cycle Hours Used: {trip_data['cycle_hours_used']} hrs")
    c.save()
    return output_path
