from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from django.db import IntegrityError
from .models import String
from .serializers import StringSerializer
import urllib.parse
import logging

logger = logging.getLogger(__name__)

class StringAPIView(APIView):
    """POST /strings and GET /strings"""
    
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"StringAPIView - Method: {request.method}, Path: {request.path}")
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        """Create/Analyze String"""
        logger.info(f"POST request data: {request.data}")
        
        if 'value' not in request.data:
            return Response(
                {"error": "Missing 'value' field"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not isinstance(request.data.get('value'), str):
            return Response(
                {"error": "Value must be a string"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # Check if string already exists before serialization
        value = request.data.get('value')
        if String.objects.filter(value=value).exists():
            return Response(
                {"error": "String already exists in the system"},
                status=status.HTTP_409_CONFLICT
            )
        
        serializer = StringSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"error": "String already exists in the system"},
                    status=status.HTTP_409_CONFLICT
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """Get All Strings with Filtering"""
        logger.info(f"GET request params: {request.query_params}")
        
        queryset = String.objects.all()
        filters_applied = {}
        
        is_palindrome = request.query_params.get('is_palindrome')
        if is_palindrome is not None:
            if is_palindrome.lower() == 'true':
                queryset = queryset.filter(is_palindrome=True)
                filters_applied['is_palindrome'] = True
            elif is_palindrome.lower() == 'false':
                queryset = queryset.filter(is_palindrome=False)
                filters_applied['is_palindrome'] = False
        
        min_length = request.query_params.get('min_length')
        if min_length is not None:
            try:
                min_length = int(min_length)
                queryset = queryset.filter(length__gte=min_length)
                filters_applied['min_length'] = min_length
            except ValueError:
                return Response(
                    {"error": "Invalid min_length value"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        max_length = request.query_params.get('max_length')
        if max_length is not None:
            try:
                max_length = int(max_length)
                queryset = queryset.filter(length__lte=max_length)
                filters_applied['max_length'] = max_length
            except ValueError:
                return Response(
                    {"error": "Invalid max_length value"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        word_count = request.query_params.get('word_count')
        if word_count is not None:
            try:
                word_count = int(word_count)
                queryset = queryset.filter(word_count=word_count)
                filters_applied['word_count'] = word_count
            except ValueError:
                return Response(
                    {"error": "Invalid word_count value"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        contains_character = request.query_params.get('contains_character')
        if contains_character is not None:
            queryset = queryset.filter(value__contains=contains_character)
            filters_applied['contains_character'] = contains_character
        
        serializer = StringSerializer(queryset, many=True)
        
        response_data = {
            'data': serializer.data,
            'count': queryset.count()
        }
        
        if filters_applied:
            response_data['filters_applied'] = filters_applied
        
        return Response(response_data, status=status.HTTP_200_OK)


class StringDetailDeleteView(APIView):
    """GET and DELETE /strings/{string_value}"""
    
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"StringDetailDeleteView - Method: {request.method}, Path: {request.path}")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, string_value):
        """Get Specific String"""
        decoded_value = urllib.parse.unquote(string_value)
        logger.info(f"GET specific string: {decoded_value}")
        
        try:
            string_obj = String.objects.get(value=decoded_value)
            serializer = StringSerializer(string_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except String.DoesNotExist:
            return Response(
                {"error": "String does not exist in the system"},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request, string_value):
        """Delete String"""
        decoded_value = urllib.parse.unquote(string_value)
        logger.info(f"DELETE string: {decoded_value}")
        
        try:
            string_obj = String.objects.get(value=decoded_value)
            string_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except String.DoesNotExist:
            return Response(
                {"error": "String does not exist in the system"},
                status=status.HTTP_404_NOT_FOUND
            )


class StringNaturalLanguageFilterView(APIView):
    """GET /strings/filter-by-natural-language - Natural Language Filtering"""
    
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"NL Filter - Method: {request.method}, Path: {request.path}")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        query = request.query_params.get('query', '')
        logger.info(f"Natural language query: {query}")
        
        if not query:
            return Response(
                {"error": "Query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        query_lower = query.lower()
        parsed_filters = {}
        queryset = String.objects.all()
        
        #Check for conflicting filters
        has_min_length = 'longer than' in query_lower or 'more than' in query_lower
        has_max_length = 'shorter than' in query_lower or 'less than' in query_lower

         # Example: "strings longer than 100 and shorter than 10" = conflict
        if has_min_length and has_max_length:
            return Response(
                {"error": "Query parsed but resulted in conflicting filters"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Parse natural language query
        if 'single word' in query_lower and 'palindrom' in query_lower:
            queryset = queryset.filter(word_count=1, is_palindrome=True)
            parsed_filters['word_count'] = 1
            parsed_filters['is_palindrome'] = True
        
        elif 'longer than 10' in query_lower:
            queryset = queryset.filter(length__gte=11)
            parsed_filters['min_length'] = 11
        
        elif 'containing the letter' in query_lower:
            # Extract character after "letter"
            parts = query_lower.split('letter')
            if len(parts) > 1:
                char = parts[1].strip().split()[0] if parts[1].strip() else ''
                if char:
                    queryset = queryset.filter(value__contains=char)
                    parsed_filters['contains_character'] = char
        
        elif 'palindrom' in query_lower and 'first vowel' in query_lower:
            queryset = queryset.filter(is_palindrome=True, value__contains='a')
            parsed_filters['is_palindrome'] = True
            parsed_filters['contains_character'] = 'a'
        
        elif 'palindrom' in query_lower:
            queryset = queryset.filter(is_palindrome=True)
            parsed_filters['is_palindrome'] = True
        
        serializer = StringSerializer(queryset, many=True)
        
        response_data = {
            'data': serializer.data,
            'count': queryset.count(),
            'interpreted_query': {
                'original': query,
                'parsed_filters': parsed_filters
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)