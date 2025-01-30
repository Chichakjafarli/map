from django.urls import path
from .views import upload_excel_view, send_top_5_emails

urlpatterns = [
    path('dashboard/', upload_excel_view, name='dashboard'),
    path('send-top-5-emails/', send_top_5_emails, name='send_top_5_emails'),  # Yeni URL əlavə olundu
]
