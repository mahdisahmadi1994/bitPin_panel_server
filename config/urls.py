
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from api.controller.authentication_controller import LoginView, RegisterView
from api.controller.post_controller import PostListView
from api.controller.rating_controller import RatePostView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('rate/<int:post_id>/', RatePostView.as_view(), name='rate-post'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
