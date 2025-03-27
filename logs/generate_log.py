import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

# Constants for Log Grid
LOG_START_X = 100  # Adjust based on template
LOG_START_Y = 400  # Adjust based on template
HOUR_BLOCK_WIDTH = 25  # Adjust width of each hour block
ROW_HEIGHTS = {
    "Off Duty": 500,
    "Sleeper Berth": 450,
    "Driving": 400,
    "On Duty": 350
}

def generate_eld_log(trip_data, output_path, template_path="blank-paper-log.png"):
    """Generates an ELD log sheet PDF with trip details drawn onto it."""
    print("🚀 Generating ELD Log...")

    # Get absolute path of the image
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, template_path)

    # Ensure the image exists
    if not os.path.exists(image_path):
        print(f"❌ Error: Image not found at {image_path}")
        return None
    # Ensure the directory exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)


    # Load the blank log sheet
    try:
        img = Image.open(image_path)
        img_width, img_height = img.size
        print(f"✅ Image Loaded Successfully: {image_path} ({img_width}x{img_height})")
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return None

    # Create PDF Canvas
    c = canvas.Canvas(output_path, pagesize=letter)

    # Ensure proper image scaling
    page_width, page_height = letter
    img_reader = ImageReader(img)

    # Scale image to fit page
    scaled_width = min(img_width, page_width) * 0.9
    scaled_height = min(img_height, page_height) * 0.9

    # Draw the image onto the PDF
    try:
        c.drawImage(img_reader, 20, 100, width=scaled_width, height=scaled_height)
        print("✅ Image Drawn on PDF Successfully")
    except Exception as e:
        print(f"❌ Error drawing image on PDF: {e}")
        return None

    # Draw Trip Details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 750, f"Trip Log: {trip_data.get('pickup_location', 'N/A')} → {trip_data.get('dropoff_location', 'N/A')}")
    c.drawString(100, 730, f"Cycle Hours Used: {trip_data.get('current_cycle_used', 0)} hrs")

    # Draw ELD Log Grid
    c.setStrokeColorRGB(1, 0, 0)  # Red color for logs
    hours = trip_data.get("hours", [])

    print("🔍 Drawing Log Lines on PDF...")
    for i, (hour, status) in enumerate(hours):
        x = LOG_START_X + (i * HOUR_BLOCK_WIDTH)
        y = ROW_HEIGHTS.get(status, LOG_START_Y)
        c.line(x, y, x + HOUR_BLOCK_WIDTH, y)  # Draw horizontal log line
        print(f"🖊️ Drawing {status} log at Hour {hour}: ({x}, {y})")

    # Save the PDF
    c.save()
    print(f"✅ PDF Successfully Generated: {output_path}")

    return output_path
