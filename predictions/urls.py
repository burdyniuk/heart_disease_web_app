from django.urls import path
from .views import prediction_input_view


urlpatterns = [
    path('input/', prediction_input_view, name='prediction_input'),
]
