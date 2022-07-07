from django.urls import path,include
# from .views import ApartmentView, ApartmentList
from .views import ApartmentView
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("apartment", views.ApartmentViewSet, "apartment")


urlpatterns = [
    path('', include(router.urls)),

    path('api/v2/apartment/', views.ApartmentView.as_view(), name="apartment"),
    path('api/v2/apartment/<int:id>', views.ApartmentView.as_view(), name="apartment"),

]
