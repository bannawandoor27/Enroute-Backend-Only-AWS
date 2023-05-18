from django.contrib import admin
from django.utils.html import format_html
from .models import Package, Itinerary, PackageImage, Review, Wishlist


class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 5


class PackageImageInline(admin.TabularInline):
    model = PackageImage
    extra = 5


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'main_place', 'duration', 'average_rating', 'total_reviews', 'price', 'discount_percent', 'type', 'is_active', 'view_itinerary_pdf')
    list_filter = ('category', 'main_place', 'is_active')
    search_fields = ('name', 'category', 'main_place')
    inlines = [ItineraryInline, PackageImageInline, ReviewInline]

    def view_itinerary_pdf(self, obj):
        if obj.itinerary_pdf:
            return format_html("<a href='{}'>View PDF</a>", obj.itinerary_pdf.url)
        else:
            return "-"
    view_itinerary_pdf.short_description = "Itinerary PDF"


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('package', 'day', 'activity')
    list_filter = ('package__name',)
    search_fields = ('package__name', 'day')


@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    list_display = ('package', 'image_preview')
    list_filter = ('package__name',)

    def image_preview(self, obj):
        return format_html("<img src='{}' width='100' height='100' />", obj.image.url)
    image_preview.short_description = "Image Preview"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'rating', 'created_at')
    list_filter = ('user__email', 'package__name')
    search_fields = ('user__email', 'package__name')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'packages_count', 'added_at', 'is_active')
    list_filter = ('user__email', 'is_active')
    search_fields = ('user__email',)

    def packages_count(self, obj):
        return obj.packages.count()
    packages_count.short_description = "Packages Count"
