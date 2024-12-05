from dao.post_dao import PostDao
from database.models import Rating


class PostLogic():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.post_dao = PostDao()

    def create_post(self,post_dict):
        return self.post_dao.create_post(title=post_dict.get("title"), content=post_dict.get("content"))


    def get_post_with_ratings_and_user(self, user):

        posts = self.post_dao.get_post_ratings(user)

        return posts