from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="folders")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Document(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=100)
    link = models.URLField()

    def __str__(self):
        return self.title

# core/models.py
from django.db import models
from django.contrib.auth.models import User

class UploadedPDF(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pdfs")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # store extracted text (nullable until extracted)
    raw_text = models.TextField(blank=True, null=True)

    # If you previously used summary/flashcards fields, keep them or add as needed
    summary = models.TextField(blank=True, null=True)
    created_mcqs = models.JSONField(blank=True, null=True)
    flashcards = models.JSONField(blank=True, null=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.user.username})"
