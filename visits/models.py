from django.db import models

class Visit(models.Model):
    cif = models.CharField(max_length=50)
    contract_number = models.CharField(max_length=50)
    address = models.TextField()
    borrower = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    region = models.CharField(max_length=100)
    region_manager = models.CharField(max_length=100)
    responsible_person = models.CharField(max_length=100)
    contact_type = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    meeting_place = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    employee_name = models.CharField(max_length=100)
    travel_date = models.DateField()
    month = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    overdue_days = models.IntegerField()
    latitude = models.FloatField(blank=True, null=True)  # Xəritə üçün enlik
    longitude = models.FloatField(blank=True, null=True) 
    is_sent = models.BooleanField(default=False)# Xəritə üçün uzunluq

    def save(self, *args, **kwargs):
        # Enlik və uzunluğu location sahəsindən avtomatik olaraq əldə etmək
        if self.location and not (self.latitude and self.longitude):
            from geopy.geocoders import Nominatim
            geolocator = Nominatim(user_agent="visitmap")
            location = geolocator.geocode(self.location)
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude
        super().save(*args, **kwargs)

    def __str__(self):
        return self.borrower
