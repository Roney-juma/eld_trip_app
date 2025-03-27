from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image

# Constants for log sheet layout
LOG_START_X = 50
LOG_START_Y = 400
HOUR_BLOCK_WIDTH = 20  # Width for each hour block
ROW_HEIGHTS = {
    "Off Duty": 340,
    "Sleeper Berth": 320,
    "Driving": 300,
    "On Duty": 280,
}

def generate_eld_log(trip_data, output_path, template_path="blank-paper-log.png"):
    """Draws trip data onto the ELD log template and exports it as a PDF."""
    
    # Load the blank log sheet
    img = Image.open(template_path)
    img_width, img_height = img.size

    # Create a new PDF with the image background
    c = canvas.Canvas(output_path, pagesize=letter)
    c.drawImage(ImageReader(img), 0, 0, width=img_width / 2, height=img_height / 2)

    # Trip Details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 750, f"Trip Log: {trip_data['pickup_location']} → {trip_data['dropoff_location']}")
    c.drawString(100, 730, f"Cycle Hours Used: {trip_data['cycle_hours_used']} hrs")

    # ELD Log Grid Drawing
    c.setStrokeColorRGB(1, 0, 0)  # Red line for logs
    hours = trip_data.get("hours", [])

    # Draw the timeline (Assume `hours` is a list of (hour, status) tuples)
    for i, (hour, status) in enumerate(hours):
        x = LOG_START_X + (i * HOUR_BLOCK_WIDTH)
        y = ROW_HEIGHTS.get(status, LOG_START_Y)
        c.line(x, y, x + HOUR_BLOCK_WIDTH, y)  # Draw the horizontal log line

    # Save the PDF
    c.save()
    return output_path

