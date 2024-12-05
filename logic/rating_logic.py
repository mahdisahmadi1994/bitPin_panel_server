from datetime import timedelta
from django.utils.timezone import now
from dao.rating_dao import RatingDao


class RatingLogic():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rating_dao = RatingDao()
        self.user_last_rating_time = {}
        self.rating_history = {}


    def add_score_for_post(self, post_id, user, score):
        return self.rating_dao.create_or_update_score_post_by_post_id_from_user(score=score, post_id=post_id, user=user)

    def rating_post(self, user, post_id, score):
        current_time = now()

        if user not in self.user_last_rating_time:
            self.user_last_rating_time[user] = self.rating_dao.get_last_rating_time_user(user=user, post_id=post_id)

        if user in self.user_last_rating_time:
            time_diff = current_time - self.user_last_rating_time[user]
            if time_diff < timedelta(seconds=30):
                return f"Rate limit exceeded. Please try again later."

        avg_score, std_dev = self.rating_dao.get_avg_std_post_by_post_id(post_id=post_id)
        if std_dev is None:
            std_dev = 0

        if std_dev == 0:
            if abs(score - avg_score) > 2:
                return f"Your score deviates significantly from the average."
        else:
            if abs(score - avg_score) > 2 * std_dev:
                return f"Your score deviates significantly from the average."

        time_diff = current_time - self.user_last_rating_time[user]
        weight = self.get_weight_with_time_diff(time_diff=time_diff)

        weighted_ratings = score * weight
        if weighted_ratings == 0:
            return f"You can't add a score because your request didn't meet the required interval."
        else:
            rating, created = self.rating_dao.create_or_update_score_post_by_post_id_from_user(user=user,
                                                                                               post_id=post_id,
                                                                                               score=weighted_ratings)
            return rating, created



    def get_weight_with_time_diff(self, time_diff):
        if time_diff <= timedelta(minutes=10):
            return 0
        return 1
