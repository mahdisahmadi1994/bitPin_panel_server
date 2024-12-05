import json

from django.db.models import Count, Avg, F, OuterRef, Subquery
from django.core.cache import cache
from database.models import Post, Rating


class PostDao():

    def get_post_ratings(self,user):
        cache_key = f'posts:list:{user.id}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return json.loads(cached_data)

        posts = Post.objects.annotate(
                 rating_count=Count('ratings'),
                 average_rating=Avg('ratings__score'),
                 user_rating=Subquery(
                    Rating.objects.filter(post=OuterRef('pk'), user=user)
                    .values('score')[:1])
                    ).values('id', 'title', 'rating_count', 'average_rating', 'user_rating')


        cache.set(cache_key,json.dumps(list(posts)), timeout = 3600)

        return posts



    def create_post(self,title, content):
        new_post = Post.objects.create(title=title, content=content)

        return new_post

