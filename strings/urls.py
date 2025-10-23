
from django.urls import path
from .views import StringAPIView, StringDetailDeleteView, StringNaturalLanguageFilterView

urlpatterns = [
    path('strings/filter-by-natural-language', StringNaturalLanguageFilterView.as_view()),
    path('strings/<path:string_value>', StringDetailDeleteView.as_view()),
    path('strings', StringAPIView.as_view()),
]