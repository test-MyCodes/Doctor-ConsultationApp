from django.contrib import admin

from users.models import notAvailableTablets, patientDetails

# Register your models here.
admin.site.register(patientDetails)
admin.site.register(notAvailableTablets)
