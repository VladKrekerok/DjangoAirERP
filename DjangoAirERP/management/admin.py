from django.contrib import admin

from .models import Option


@admin.register(Option)
class StaffAdmin(admin.ModelAdmin):
    list_display = ["option", "price", "weight", "service_type"]
