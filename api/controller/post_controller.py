from django.db.models.base import method_get_order
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializer.post_serializer import PostListSerializer, PostCreateSerializer
from logic.post_logic import PostLogic


class PostListView(APIView):

    def get_permissions(self):
        if self.request.method == 'get':
            return [IsAuthenticated()]
        return []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.post_logic = PostLogic()

    def post(self,request):
        serializer = PostCreateSerializer(data=request.data)

        if serializer.is_valid():
            self.post_logic.create_post(serializer.data)

            return Response({
                'message': 'Post created successfully.',
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        posts =self.post_logic.get_post_with_ratings_and_user(request.user)
        serializer = PostListSerializer(posts, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


