from django.shortcuts import render
from .models import QRCode
import qrcode
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
import os

def generate_qr(request):
    # Initialize variables for QR image URL and error message
    qr_image_url = None
    error = None

    # Check if the request method is POST (form submitted)
    if request.method == "POST":
        # Get data from form fields
        mobile_number = request.POST.get('mobile_number')
        data = request.POST.get('qr_data')

        # Validate mobile number: must be exactly 10 digits and numeric
        if not mobile_number or len(mobile_number) != 10 or not mobile_number.isdigit():
            error = "Invalid Mobile Number"
        else:
            # Prepare the data string to encode in the QR code
            qr_content = f"{data}|{mobile_number}"

            # Generate the QR code image in memory
            qr = qrcode.make(qr_content)
            qr_image_io = BytesIO()
            qr.save(qr_image_io, format='PNG')
            qr_image_io.seek(0)  # Reset pointer to the beginning of the stream

            # Create directory inside MEDIA_ROOT to save the QR image
            qr_storage_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
            os.makedirs(qr_storage_path, exist_ok=True)

            # Save the QR image using Django's file storage system
            fs = FileSystemStorage(location=qr_storage_path, base_url='/media/qr_codes/')
            filename = f"{data}_{mobile_number}.png"
            qr_image_content = ContentFile(qr_image_io.read(), name=filename)
            fs.save(filename, qr_image_content)

            # Get the URL of the saved QR image to show on the frontend
            qr_image_url = fs.url(filename)

            # Save the data and mobile number to the database using the QRCode model
            QRCode.objects.create(data=data, mobile_number=mobile_number)

    # Render the template and pass the QR image URL and error message (if any)
    return render(request, 'scanner/generate.html', {
        'qr_image_url': qr_image_url,
        'error': error
    })

# Create your views here.
def scan_qr(request):
    return render(request,'scanner/scanner.html')