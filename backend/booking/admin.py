from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import format_html

from .models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = (
   
        'user',
        'package',
        'phone_number',
        'start_date',
        'end_date',
        'num_adults',
        'num_infants',
        'num_children',
        'status',
        'payment',
    )
    list_filter = (
        'package',
        'status',
    )
    search_fields = (
        'user__email',
        'booking_code',
    )
    readonly_fields = (
        'booking_code',
        'user',
        'package',
        'date_booked',
        'start_date',
        'end_date',
        'num_adults',
        'num_infants',
        'num_children',
        'phone_number',
        'status',
        'payment',
    )
    fieldsets = (
        (_('Booking Information'), {
            'fields': (
                'booking_code',
                'user',
                'package',
                'date_booked',
                'status',
            )
        }),
        (_('Stay Dates and Guests'), {
            'fields': (
                'start_date',
                'end_date',
                'num_adults',
                'num_infants',
                'num_children',
            )
        }),
        (_('Contact Details'), {
            'fields': (
                'phone_number',
            )
        }),
        (_('Payment Details'), {
            'fields': (
                'payment',
            )
        }),
    )

    def get_package_link(self, obj):
        url = reverse('admin:packages_package_change', args=[obj.package.id])
        return format_html('<a href="{}">{}</a>', url, obj.package.name)
    get_package_link.short_description = _('Package')

    def get_payment_link(self, obj):
        if obj.payment:
            url = reverse('admin:payments_payment_change', args=[obj.payment.id])
            return format_html('<a href="{}">{}</a>', url, obj.payment.razorpay_order_id)
    get_payment_link.short_description = _('Payment')


admin.site.register(Booking, BookingAdmin)
