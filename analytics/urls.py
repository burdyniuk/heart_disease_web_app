from django.urls import path
from analytics.views import analytics_view


urlpatterns = [
	path('analytics/', analytics_view, name='analytics_view'),
]
