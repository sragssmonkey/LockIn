from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("pomodorotimer/", views.pomodoro, name="pomodoro"),
    path("habittracker/", views.habit, name="habit"),
    path("notebook/", views.notebook, name="notebook"),

    # PDF Upload + Detail pages
    path("upload_pdf/", views.upload_pdf, name="upload_pdf"),
    path("pdf_detail/<int:pk>/", views.pdf_detail, name="pdf_detail"),  # ✅ FIXED
    path("generate_quiz/<int:pk>/", views.generate_quiz, name="generate_quiz"),

    # Auth
    path("signup/", views.signup, name="signup"),
]
