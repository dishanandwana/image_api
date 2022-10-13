from rest_framework import serializers
from task.models import Image, reimage

class ImageSerializer(serializers.ModelSerializer): 
    class Meta: 

        model = Image

        fields = ['id','image']


class ReimageSerializer(serializers.ModelSerializer):
    class Meta:
        model=reimage
        fields=['gray','large','medium','thumbnail']
   

    