from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import EmailMessage
from .forms import ExcelUploadForm
from .models import Visit
from .utils import import_excel

def upload_excel_view(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Excel faylını əldə edin
            excel_file = request.FILES['file']
            
            # Excel faylını emal edin və məlumatları bazaya əlavə edin
            import_excel(excel_file)
            
            # Bütün məlumatları bazadan götür
            visits = Visit.objects.all()
            return render(request, 'visits/dashboard.html', {'visits': visits, 'form': form})
    else:
        form = ExcelUploadForm()
    
    # GET sorğuları ilə filtr tətbiqi
    cif_query = request.GET.get('cif', '')  # CİF axtarış sorğusu
    overdue_query = request.GET.get('overdue_days', 'all')
    amount_query = request.GET.get('amount', 'all')

    # Filtrləmə məntiqi
    visits = Visit.objects.all()

    if cif_query:
        visits = visits.filter(cif__icontains=cif_query)  # CİF axtarışı

    if overdue_query != 'all':
        visits = visits.filter(overdue_days__lte=int(overdue_query))  # Gecikmə günlərinə görə filtr

    if amount_query != 'all':
        visits = visits.filter(amount__lte=int(amount_query))  # Məbləğə görə filtr

    return render(request, 'visits/dashboard.html', {'visits': visits, 'form': form})

def send_top_5_emails(request):
    if request.method == 'POST':
        # Top 5 prioritetli müştəriləri seç və təkrarlanmamaq üçün distinct() istifadə et
        top_visits = Visit.objects.filter(is_sent=False).order_by('-amount', '-overdue_days')[:5]

        # Email məzmununu hazırla
        email_subject = "Prioritetli Müştərilər"
        email_body = "Aşağıdakı müştərilər prioritetlidir:\n\n"
        seen_visits = set()  # Duplikatları izləmək üçün

        for visit in top_visits:
            # Duplikatların qarşısını almaq üçün yoxlayırıq
            if (visit.borrower, visit.amount, visit.overdue_days, visit.address) not in seen_visits:
                email_body += (
                    f"Ad: {visit.borrower}, Məbləğ: {visit.amount}, "
                    f"Gecikmə Günləri: {visit.overdue_days}, Ünvan: {visit.address}\n"
                )
                seen_visits.add((visit.borrower, visit.amount, visit.overdue_days, visit.address))

        # Email göndər
        email = EmailMessage(
            email_subject,
            email_body,
            'banujafarli9@gmail.com',  # Göndərən
            ['chichakjafarli2000@gmail.com']  # Alıcı
        )
        email.send(fail_silently=False)

        # Göndərilən müştəriləri yenilə
        for visit in top_visits:
            visit.is_sent = True
            visit.save()

        return JsonResponse({'message': 'Top 5 müştəriyə mail göndərildi!'})
