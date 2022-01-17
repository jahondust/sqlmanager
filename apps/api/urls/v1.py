from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('queries/', include(('apps.api.queries.urls', 'apps.queries'))),
    path('me/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('me/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
