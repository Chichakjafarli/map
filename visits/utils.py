import pandas as pd
from .models import Visit
from geopy.geocoders import Nominatim

def import_excel(file):
    geolocator = Nominatim(user_agent="visitmap")
    data = pd.read_excel(file)

    for _, row in data.iterrows():
        latitude, longitude = None, None
        if row['location']:
            location = geolocator.geocode(row['location'])
            if location:
                latitude = location.latitude
                longitude = location.longitude

        # Bazaya məlumatları əlavə et
        Visit.objects.create(
            cif=row['cif'],
            contract_number=row['contract_number'],
            address=row['address'],
            borrower=row['borrower'],
            location=row['location'],
            region=row['region'],
            region_manager=row['region_manager'],
            responsible_person=row['responsible_person'],
            contact_type=row['contact_type'],
            contact_person=row['contact_person'],
            meeting_place=row['meeting_place'],
            notes=row['notes'],
            employee_name=row['employee_name'],
            travel_date=row['travel_date'],
            month=row['month'],
            amount=row['amount'],
            overdue_days=row['overdue_days'],
            latitude=latitude,
            longitude=longitude
        )
