from django.urls import path, re_path
from .views import (
    StringAPIView,
    StringDetailDeleteView,
    StringNaturalLanguageFilterView
)

urlpatterns = [
    
    path('strings/filter-by-natural-language', StringNaturalLanguageFilterView.as_view(), name='string-nl-filter'),
   
    re_path(r'^strings/(?P<string_value>.+)$', StringDetailDeleteView.as_view(), name='string-detail-delete'),
    
    path('strings', StringAPIView.as_view(), name='string-api'),
]