# core/views.py
import os
import json
import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings

from .forms import PDFUploadForm
from .models import UploadedPDF
from .groq_client import generate_mcqs
# core/views.py (add/imports at top)
from django.http import JsonResponse
from .groq_client import generate_mcqs
from .models import UploadedPDF
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def generate_quiz(request, pk):
    pdf = get_object_or_404(UploadedPDF, pk=pk, user=request.user)

    mcq_data = generate_mcqs(pdf.raw_text, num_questions=5)

    # handle backend errors
    if "error" in mcq_data:
        return JsonResponse({"error": mcq_data["error"]})

    # ensure we always return list
    mcqs = mcq_data.get("mcqs", [])
    if not isinstance(mcqs, list):
        return JsonResponse({"error": "MCQ format invalid"})

    return JsonResponse({"mcqs": mcqs})




# Use environment variable or Django settings
PDFCO_API_KEY = getattr(settings, "PDFCO_API_KEY", os.environ.get("PDFCO_API_KEY"))


def home(request):
    return render(request, 'core/home.html')


def pomodoro(request):
    return render(request, 'core/pomodoro.html')


def habit(request):
    return render(request, 'core/habit.html')


def notebook(request):
    return render(request, 'core/notebook.html')


# --------------------
# Signup (unchanged)
# --------------------
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    else:
        form = UserCreationForm()
    return render(request, "core/signup.html", {"form": form})


# --------------------
# PDF upload & extraction
# --------------------

from .utils import extract_text_from_pdf

@login_required
def upload_pdf(request):
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user

            # Extract text locally
            extracted_text = extract_text_from_pdf(request.FILES["file"])
            obj.raw_text = extracted_text
            obj.save()

            return redirect("pdf_detail", pk=obj.pk)
    else:
        form = PDFUploadForm()

    return render(request, "core/upload_pdf.html", {"form": form})



@login_required
def pdf_detail(request, pk):
    """
    Show the uploaded PDF object, including raw_text.
    Frontend JS can take raw_text and build flashcards in-browser.
    """
    pdf = get_object_or_404(UploadedPDF, pk=pk, user=request.user)
    return render(request, 'core/pdf_detail.html', {'pdf': pdf})


# --------------------
# Helper: talk to PDF.co
# --------------------
def _extract_text_via_pdfco(file_obj):
    PDFCO_API_KEY = settings.PDFCO_API_KEY

    if not PDFCO_API_KEY:
        raise RuntimeError("PDFCO_API_KEY not set in settings or environment")

    upload_url = "https://api.pdf.co/v1/file/upload"
    headers = {"x-api-key": PDFCO_API_KEY}

    # Read file content
    file_bytes = file_obj.read()

    # PDF.co requires tuple: (filename, file_bytes, mime)
    files = {
        "file": (file_obj.name, file_bytes, "application/pdf")
    }

    # Upload the file
    upload_res = requests.post(upload_url, headers=headers, files=files)

    try:
        upload_json = upload_res.json()
    except:
        raise RuntimeError("Upload failed: " + upload_res.text)

    if not upload_json.get("url"):
        raise RuntimeError("Upload failed: " + str(upload_json))

    file_url = upload_json["url"]

    # Now extract text
    extract_url = "https://api.pdf.co/v1/pdf/convert/to/text"
    payload = {"url": file_url}

    extract_res = requests.post(extract_url, headers=headers, json=payload)
    extract_json = extract_res.json()

    if extract_json.get("error"):
        raise RuntimeError("Extraction failed: " + extract_json.get("message", "Unknown error"))

    return extract_json.get("body", "")
