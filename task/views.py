from django.shortcuts import render
from rest_framework import generics
from .models import Image as ime,reimage
from . serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from PIL import Image as abc
from io import BytesIO
from django.core.files.base import ContentFile


# Create your views here.
class ImageCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    model = ime
    
    serializer_class = ImageSerializer
    queryset = ime.objects.all()

    def post(self, request):

        serializer = ImageSerializer(data=request.data) 

   

        if serializer.is_valid():
            serializer.save()

            getting_img_url=ime.objects.get(id=serializer.data['id'])


            


            # grayscale image
            img_io = BytesIO() 

            img = abc.open(getting_img_url.image.path).convert('L')  #grayscale image

           # img.save('greyscale.png')
            img = img.convert('RGB')
            img.save(img_io, format='JPEG', quality=100)

            img_content_gray = ContentFile(img_io.getvalue(), 'grayimage.png')

            img_io1=BytesIO()
            img1 = abc.open(getting_img_url.image.path)   

          
          # for Large image
            image1 = img1.resize((1024,768),abc.ANTIALIAS)  #large image
            #image1.save(fp="largeimage.png")
            image1 = image1.convert('RGB')
            image1.save(img_io1, format='JPEG', quality=100)

            img_content_large = ContentFile(img_io1.getvalue(), 'largeimage.png')


        # for medium image
            image2 = img1.resize((500,500),abc.ANTIALIAS)   #medium image
            #image2.save(fp="mediumimage.png")
            img_io2=BytesIO()
            image2 = image2.convert('RGB')
            image2.save(img_io2, format='JPEG', quality=100)
            img_content_medium = ContentFile(img_io2.getvalue(), 'mediumimage.png')
            

         # thumbnail image
            image3=img1.resize((200,300),abc.ANTIALIAS)     #thumbnail image
            img_io3=BytesIO()
            image3 = image3.convert('RGB')
            image3.save(img_io3, format='JPEG', quality=100)
            img_content = ContentFile(img_io3.getvalue(), 'thumb.png')

            eobj=reimage.objects.create(gray=img_content_gray,large=img_content_large,medium=img_content_medium,thumbnail=img_content)
            eobj.save()
           
        
            
            seri=reimage.objects.filter(id=eobj.id)
            
            serializer =ReimageSerializer(seri, context={"request": request}, many=True)
            # return Response(serializer.data)


            
            return Response({
                'status': True, 
                 'message': 'Image Upload Successfully',
                'data': serializer.data, 
            }, status = status.HTTP_201_CREATED)

        else:
            return Response({
            'status': False,
            'message': 'Error! Make sure image field is not empty',
            }, status = status.HTTP_400_BAD_REQUEST)




