from django.contrib import admin

from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'active', 'valid_from', 'valid_to']
    list_filter = ['active', 'valid_to', 'valid_from']
    list_editable = ['active']
