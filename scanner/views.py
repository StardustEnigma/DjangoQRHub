from django.shortcuts import render
from .models import QRCode
import qrcode
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
import os
from pyzbar.pyzbar import decode
from pathlib import Path
from PIL import Image

# ------------------------- QR Code Generation View -------------------------

def generate_qr(request):
    # Initialize variables for the QR image URL and any error messages
    qr_image_url = None
    error = None

    # Handle POST request when the form is submitted
    if request.method == "POST":
        mobile_number = request.POST.get('mobile_number')
        data = request.POST.get('qr_data')

        # Basic mobile number validation (must be exactly 10 digits)
        if not mobile_number or len(mobile_number) != 10 or not mobile_number.isdigit():
            error = "Invalid Mobile Number"
        else:
            # Format content to be embedded into the QR code
            qr_content = f"{data}|{mobile_number}"

            # Generate the QR image using qrcode library
            qr = qrcode.make(qr_content)
            qr_image_io = BytesIO()
            qr.save(qr_image_io, format='PNG')
            qr_image_io.seek(0)  # Reset stream position

            # Define folder path to store QR images (inside MEDIA_ROOT)
            qr_storage_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
            os.makedirs(qr_storage_path, exist_ok=True)

            # Save QR image to the file system
            fs = FileSystemStorage(location=qr_storage_path, base_url='/media/qr_codes/')
            filename = f"{data}_{mobile_number}.png"
            qr_image_content = ContentFile(qr_image_io.read(), name=filename)
            fs.save(filename, qr_image_content)

            # Generate URL to display the saved image in frontend
            qr_image_url = fs.url(filename)

            # Save the QR code data into the database
            QRCode.objects.create(data=data, mobile_number=mobile_number)

    # Render the template and pass any result or error
    return render(request, 'scanner/generate.html', {
        'qr_image_url': qr_image_url,
        'error': error
    })


# ------------------------- QR Code Scanning View -------------------------

def scan_qr(request):
    result = None  # Will hold the result message
    error = None   # Can be used for error handling if needed

    # Handle POST request with uploaded file
    if request.method == "POST" and request.FILES.get('qr_image'):
        print(request.FILES)  # Debug print of uploaded files

        mobile_number = request.POST.get('mobile_number')
        qr_image = request.FILES.get('qr_image')

        # Validate the mobile number
        if not mobile_number or len(mobile_number) != 10 or not mobile_number.isdigit():
            result = "Invalid Mobile Number"
        else:
            # Save the uploaded image temporarily to disk
            fs = FileSystemStorage()
            filename = fs.save(qr_image.name, qr_image)
            image_path = Path(fs.location) / filename

            try:
                # Open and decode the QR image
                image = Image.open(image_path)
                decoded_objects = decode(image)

                if decoded_objects:
                    qr_content = decoded_objects[0].data.decode('utf-8').strip()

                    # Check QR content format
                    if '|' in qr_content:
                        qr_data, qr_mobile_number = qr_content.split('|')

                        # Validate against database
                        qr_entry = QRCode.objects.filter(data=qr_data, mobile_number=qr_mobile_number).first()

                        # If entry exists and mobile number matches
                        if qr_entry and qr_mobile_number == mobile_number:
                            result = "✅ Scan Successful: Valid QR Code for the provided mobile number."

                            # Delete the record after successful scan
                            qr_entry.delete()

                            # Delete associated QR image from media storage
                            qr_image_path = Path(settings.MEDIA_ROOT) / 'qr_codes' / f"{qr_data}_{qr_mobile_number}.png"
                            if qr_image_path.exists():
                                qr_image_path.unlink()

                        else:
                            result = "❌ Scan Failed: Invalid QR or Mobile Number mismatch."
                    else:
                        result = "❌ QR Code format invalid."
                else:
                    result = "❌ No QR code detected in the image."

            except Exception as e:
                # Catch and display any error that occurs during image decoding
                result = f"❌ Error processing the image: {str(e)}"

            finally:
                # Always delete the temporary uploaded image
                if image_path.exists():
                    image_path.unlink()

    # Render the scan page and display the result
    return render(request, 'scanner/scanner.html', {'result': result})
