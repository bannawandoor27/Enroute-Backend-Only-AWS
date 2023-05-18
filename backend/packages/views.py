import json
from django.db.models import Q,Count,Prefetch,F
from django.db.models.functions import Coalesce
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

from booking.models import Booking
from .models import Package, PackageImage,Wishlist,Review
from .serializers import ItinerarySerializer, PackageSerializer,PackageImageSerializer, ReviewSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
import json

def get_filtered_queryset(value):
    queryset = Package.objects.filter(
        Q(name__icontains=value) |
        Q(category__icontains=value) |
        Q(main_place__icontains=value) |
        Q(places__icontains=value)
    )
    return queryset
class PackageSearchPagination(PageNumberPagination):
    page_size = 8
class PackageSearchSuggestionView(ListAPIView):
    serializer_class = PackageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category', 'main_place', 'places__icontains']

    def get_queryset(self):
        value = self.request.query_params.get('value')
        queryset = get_filtered_queryset(value)
        return queryset.values_list('name', flat=True)

    def list(self, request):
        queryset = self.get_queryset()
        return Response(queryset)
    



class PriceFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')
        if price_min and price_max:
            queryset = queryset.filter(price__gte=price_min, price__lte=price_max)
        elif price_min:
            queryset = queryset.filter(price__gte=price_min)
        elif price_max:
            queryset = queryset.filter(price__lte=price_max)
        return queryset


class PackageSearchView(ListAPIView):
    serializer_class = PackageSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, PriceFilter]
    search_fields = ['name', 'category', 'main_place', 'places__icontains', 'price','type']
    pagination_class = PackageSearchPagination

    def get_queryset(self):
        value = self.request.query_params.get('value')
        types = self.request.query_params.get('type')
        if value is None:
            queryset = self.serializer_class.Meta.model.objects.all().order_by('id')
            queryset = queryset.annotate(total_count=Count('id'))
        else:
            queryset = self.serializer_class.Meta.model.objects.filter(
                Q(name__icontains=value)
                | Q(category__icontains=value)
                | Q(main_place__icontains=value)
                | Q(places__icontains=value)
            ).order_by('id')
            queryset = queryset.annotate(total_count=Count('id'))
        if types!=None :
            if len(types)>2:
                types_list = json.loads(types)
                print(types_list)
                queryset = queryset.filter(type__in=types_list)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        unique_types = set(Package.objects.values_list('type', flat=True).distinct())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if not queryset:
                return Response(data={'error': 'No package for your requirements'}, status=status.HTTP_400_BAD_REQUEST)
            return self.get_paginated_response({'results': serializer.data, 'count': queryset[0].total_count,'unique_types': unique_types})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['GET']) 
def package_detail(request, id):
    package = get_object_or_404(Package, pk=id)
    itinerary = package.itinerary.select_related('package').all()
    reviews = package.reviews.prefetch_related('user').all()
    images = package.images.all()

    package_serializer = PackageSerializer(package,context={'request': request})

    # Create a list of image URLs
    image_urls = [request.build_absolute_uri(image.image.url) for image in images]

    package_data = {
        'packageData': package_serializer.data,
        'images': image_urls,
    }

    return Response(package_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def package_nav(request):
   category_list = list(set(list(Package.objects.values_list('category', flat=True) )))
   nav_list  = []
   for i in category_list:
      img_url  =  request.build_absolute_uri( PackageImage.objects.filter(package__category=i).first().image.url)
      nav_list.append( {'season':i,
                        'packages':list(Package.objects.filter(category=i).values_list('name',flat=True)),
                        'image':img_url
                           })
   return Response(nav_list,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request, id):
    package = Package.objects.get(pk=id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if package in wishlist.packages.all():
        wishlist.packages.remove(package)
        return Response({'success': True, 'message': 'Package removed from wishlist.'})
    else:
        wishlist.packages.add(package)
        return Response({'success': True, 'message': 'Package added to wishlist.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def wishlist_items(request):
    wishlist = Wishlist.objects.prefetch_related('packages').filter(user=request.user)
    packages = wishlist[0].packages.all()
    serializer  = PackageSerializer(packages,many=True,context={'request':request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_in_wishlist(request,id):
    try:
        package = Package.objects.get(id=id)
        wishlist = Wishlist.objects.get(user=request.user)
        if package in wishlist.packages.all():
            is_in_wishlist = True
        else:
            is_in_wishlist = False
    except:
        return Response(False)
    return Response(is_in_wishlist)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, id):
    try:
        user = request.user
        package = get_object_or_404(Package,id=id)
        if not Booking.objects.filter(user=user,package=package).exists():
            return Response({'error':'You need to book the package first'},status=status.HTTP_400_BAD_REQUEST)
        print(request.data)
        review_text = request.data['review_text']
        rating = request.data['rating']
        if review_text=='' or rating not in range(0,6):
            return Response({'error':'Please provide a valid review'},status=status.HTTP_403_FORBIDDEN)
        Review.objects.create(package=package,user=user,review_text=review_text,rating=rating)
        package.update_review_stats()
        package.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    except:
        return Response({'error':'Please try again later'},status=status.HTTP_400_BAD_REQUEST)

