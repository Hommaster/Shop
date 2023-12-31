from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'address',
                    'city', 'postal_code', 'paid']
    list_filter = ['paid', 'created', 'updated']
