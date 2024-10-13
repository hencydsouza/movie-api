from django.urls import path, include
from .views import RegisterView, MoviesListView, CollectionListView, CollectionDetailView, RequestCountView, ResetRequestCountView,CollectionViewSet
from .middleware import RequestCounterMiddleware
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'collection', CollectionViewSet, basename='collection')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('movies/', MoviesListView.as_view(), name='movies-list'),
    # path('collection/', CollectionListView.as_view(), name='collection-list'),
    # path('collection/<int:pk>/', CollectionDetailView.as_view(), name='collection-detail'),
    path('', include(router.urls)),
    path('request-count/', RequestCountView.as_view(), name='request-count'),
    path('request-count/reset/', ResetRequestCountView.as_view(), name='reset-request-count'),
]
