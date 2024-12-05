from rest_framework import serializers
from database.models import Rating

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['id', 'post', 'score']
