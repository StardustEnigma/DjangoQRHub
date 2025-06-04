from django.shortcuts import render

def generate_qr(request):
    return render(request,'scanner/generate.html')

# Create your views here.
def scan_qr(request):
    return render(request,'scanner/scanner.html')