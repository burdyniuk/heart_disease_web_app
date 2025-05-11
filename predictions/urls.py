from django.urls import path
from .views import prediction_input_view, predictions_list_view, my_predictions, export_train_data_csv


urlpatterns = [
    path('input/', prediction_input_view, name='prediction_input'),
    path('list/', predictions_list_view, name='predictions_list'),
    path('my_predictions/', my_predictions, name='my_predictions'),
    path('export_train_data_csv/', export_train_data_csv, name='export_train_data_csv'),

]
