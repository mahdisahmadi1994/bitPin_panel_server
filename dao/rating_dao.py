from django.core.cache import cache

from database.models import Rating, Post


class RatingDao():

    def create_or_update_score_post_by_post_id_from_user(self, post_id, user, score):

        rating, created = Rating.objects.update_or_create(
            post_id=post_id,
            user_id=user.id,
            defaults={'score': score}
        )

        cache_key = f'posts:list:{user.id}'
        cache.delete(cache_key)
        return rating, created


    def get_avg_std_post_by_post_id(self, post_id:int):
        posts = Rating.objects.filter(post_id=post_id).aggregate(avg_score=Avg('score'),
                                                                 std_dev=StdDev('score'))
        return posts['avg_score'], posts['std_dev']

    def get_last_rating_time_user(self, user, post_id:int):

        last_rating = Rating.objects.filter(user=user.id, post_id=post_id).order_by('timestamp').first()
        if last_rating:
            return last_rating.timestamp
        return None