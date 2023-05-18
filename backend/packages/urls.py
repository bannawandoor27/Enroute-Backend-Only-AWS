from django.urls import path
from .views import PackageSearchView,PackageSearchSuggestionView, add_review, is_in_wishlist,package_detail,package_nav,add_to_wishlist,wishlist_items
urlpatterns = [
    path('package_search/',PackageSearchView.as_view()),
    path('package_search_suggestion/',PackageSearchSuggestionView.as_view()),
    path('package_detail/<int:id>/',package_detail),
    path('package_nav/',package_nav),
    path('add_wishlist/<int:id>/',add_to_wishlist),
    path('wishlist_items/',wishlist_items),
    path('is_in_wishlist/<int:id>/',is_in_wishlist),
    path('add_review/<int:id>/',add_review),
]