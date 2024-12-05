from django.db.models import Avg
from rest_framework import serializers
from database.models import Post, Rating


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']


class PostListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    average_rating = serializers.FloatField()
    rating_count = serializers.IntegerField()
    user_rating = serializers.IntegerField(required=False, allow_null=True)


    class Meta:
        model = Post
        fields = ['id', 'title', 'average_rating', 'rating_count', 'user_rating']

