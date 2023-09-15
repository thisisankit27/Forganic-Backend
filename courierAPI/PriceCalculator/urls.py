from django.urls import path
from . import views

urlpatterns = [
    path('priceCalculate/', views.ItemDimensionsView.as_view(), name='priceCalculate'),
]