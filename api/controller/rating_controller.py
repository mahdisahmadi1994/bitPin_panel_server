from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from logic.rating_logic import RatingLogic


class RatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rating_logic = RatingLogic()

    def post(self, request, post_id):
        score = request.data.get('score')
        if not 0 <= score <= 5:
            return Response({'error' : 'Score must be between 0 and 5'})

        user = request.user
        response = self.rating_logic.rating_post(score=score, user=user, post_id=post_id)

        if isinstance(response, str):
            return Response({'error': response}, status=status.HTTP_400_BAD_REQUEST)

        rating, created = response

        if created:
            return Response({'message':'Rating saved successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'Rating update successfully.'}, status=status.HTTP_200_OK)


