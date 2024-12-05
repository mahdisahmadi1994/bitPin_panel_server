from django.http import Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db import transaction

from api.serializer.authentication_serializer import RegisterSerializer, LoginSerializer

User = get_user_model()


class RegisterView(APIView):

    @transaction.atomic()
    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                new_user = serializer.save()
                refresh = RefreshToken.for_user(new_user)
                user_data = RegisterSerializer(instance=new_user).data  # it will not trigger a new query
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user_info": user_data
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            received_username = serializer.validated_data.get("username")
            received_password = serializer.validated_data.get("password")

            try:
                the_user: User = get_object_or_404(User, username=received_username)
            except Http404:
                return Response({"detail": "Incorrect username or password"}, status=status.HTTP_401_UNAUTHORIZED)

            if the_user.check_password(received_password):

                refresh_token = RefreshToken.for_user(the_user)
                user_data = self.serializer_class(instance=the_user).data
                return Response(
                    {
                        "refresh": str(refresh_token),
                        "access": str(refresh_token.access_token),
                        "user_info": user_data
                    },
                    status=status.HTTP_200_OK
                )

            else:
                return Response({"detail": "Incorrect username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


