from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from packages.models import Package,PackageImage
from django.db.models import Count
from rest_framework.response import Response
from packages.serializers import PackageSerializer,PackageImageSerializer
from .serializers import FavoriteDestinationSerializer,CategoryPackageSerializer,VideoSerializer
from rest_framework.permissions import AllowAny
from .models import Video


@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):

    # Favorite destinations Section
    if '/favorites/' in request.path:
        package_counts_main_place = Package.objects.values('main_place').annotate(package_count=Count('id'))
        package_images_main_place = PackageImage.objects.filter(package__main_place__in=package_counts_main_place.values('main_place'))
        image_urls = {}
        for pi in package_images_main_place:
            image_urls[pi.package.main_place] = request.build_absolute_uri(pi.image.url) 

        favorite_destinations = []
        for pc in package_counts_main_place:
            image_url = image_urls.get(pc['main_place'])
            favorite_destinations.append({
                'main_place': pc['main_place'],
                'package_count': pc['package_count'],
                'image_url': image_url
            })
        serialized_favorite_destinations  = FavoriteDestinationSerializer(favorite_destinations,many=True)
        return Response(serialized_favorite_destinations.data)
    
    # Featured Packages Section
    elif '/featured/' in request.path:
        package_counts_main_place = Package.objects.values('main_place').annotate(package_count=Count('id')).order_by('-package_count')
        main_place_list = [i['main_place'] for i in package_counts_main_place]
        main_place = request.query_params.get('main_place', main_place_list[0])
        featured_packages = Package.objects.prefetch_related('images').filter(main_place = main_place)[:7]
        serialized_featured_packages = PackageSerializer(featured_packages,many=True,context={'request': request})

        return Response({'packages':serialized_featured_packages.data,'main_places':main_place_list})
    
    # Category Packages Section
    elif 'category' in request.path:
        package_counts_category = Package.objects.values('category').annotate(package_count=Count('id'))
        package_images_category = PackageImage.objects.filter(package__category__in=package_counts_category.values('category'))
        image_urls = {}
        for pi in package_images_category:
            image_urls[pi.package.category] = pi.image.url

        category_packages = []
        for pc in package_counts_category:
            image_url = image_urls.get(pc['category'])
            category_packages.append({
                'category': pc['category'],
                'package_count': pc['package_count'],
                'image_url': request.build_absolute_uri(image_url)
            })
        
        serialized_category_packages = CategoryPackageSerializer(category_packages,many=True)
        return Response(serialized_category_packages.data)
    
    elif '/videos/' in request.path:
        videos = Video.objects.all().order_by('?')[:5]
        serializer_context = {'request': request}
        serialized_videos = VideoSerializer(videos,many=True,context=serializer_context)
        return Response(serialized_videos.data)
    
    
    
        
    
   
    
    
    




    
    
    


    


