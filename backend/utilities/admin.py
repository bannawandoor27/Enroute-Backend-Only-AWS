from django.contrib import admin
from .models import Enquiry, Testimonial, Contact, CouponAssignment, Coupon
from django.contrib.admin import DateFieldListFilter

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_phone', 'checked')
    list_filter = ('checked',)
    search_fields = ('client_name', 'client_phone')

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_place', 'client_image')
    search_fields = ('client_name', 'client_place')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','message')
    search_fields = ('name', 'email')

class CouponAssignmentAdmin(admin.ModelAdmin):
    list_display = ('coupon', 'user', 'assigned_at')
    search_fields = ('coupon__coupon_name', 'user__email')
    list_filter = ('coupon', 'user')

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'coupon_name', 'is_active', 'discount_price', 'expiration_date')
    list_filter = ('is_active', ('expiration_date', DateFieldListFilter))  # Enable datepicker for expiration_date
    search_fields = ('code', 'coupon_name')


admin.site.register(Enquiry, EnquiryAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(CouponAssignment, CouponAssignmentAdmin)
