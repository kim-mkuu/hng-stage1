from django.urls import path
from .views import (
    StringAPIView,
    StringDetailDeleteView,
    StringNaturalLanguageFilterView  
)

urlpatterns = [
    path('strings/filter-by-natural-language', StringNaturalLanguageFilterView.as_view(), name='string-nl-filter'),
    path('strings/<path:string_value>', StringDetailDeleteView.as_view(), name='string-detail-delete'),
    path('strings', StringAPIView.as_view(), name='string-api'),
]