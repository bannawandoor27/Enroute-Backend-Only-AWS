from rest_framework.views import APIView
from rest_framework.response import Response
from booking.tasks import send_enquiry_async,send_whatsapp_message_async
from .models import Testimonial
from .serializers import EnquirySerializer, TestimonialSerializer
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework import status
from .serializers import ContactSerializer
from django.conf import settings



class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_whatsapp_message_async.delay(
                message=f'''
                    *Message*

                    New message received on Enroute
                    Name: {serializer.data['name']}
                    Phone: {serializer.data['email']}
                    message : {serializer.data['message']}
                ''',
                number=settings.WHATSAPP_NUM
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class EnquiryView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        enq_serializer = EnquirySerializer(data=request.data)
        if enq_serializer.is_valid():
            client_obj=enq_serializer.save()
            client_request = client_obj.client_request()
            try: 
                 send_enquiry_async.delay(client_request)
                 send_whatsapp_message_async.delay(message=client_request,number=settings.WHATSAPP_NUM)

            except:
                Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
            return Response(status=status.HTTP_201_CREATED)
        return Response(enq_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Testimonials(ListAPIView):
    queryset = Testimonial.objects.all()[:7]
    serializer_class = TestimonialSerializer


    