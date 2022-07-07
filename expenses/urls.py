from django.urls import path
from . import views


urlpatterns = [
    path('api/v2/expenses/', views.ExpenseListAPIView.as_view(), name="expenses"),
    path('api/v2/expenses/<int:id>', views.ExpenseDetailAPIView.as_view(), name="expense"),
]
