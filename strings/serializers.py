from rest_framework import serializers
from .models import String
from .utils import calculate_properties

class StringSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()
    id = serializers.CharField(source='sha256_hash', read_only=True)

    class Meta:
        model = String
        fields = ['id', 'value', 'properties', 'created_at']
        read_only_fields = ['created_at']

    def get_properties(self, obj):
        return {
            'length': obj.length,
            'is_palindrome': obj.is_palindrome,
            'unique_characters': obj.unique_characters,
            'word_count': obj.word_count,
            'sha256_hash' : obj.sha256_hash,
            'character_frequency_map' : obj.character_frequency_map
        }
    
    def validate_value(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("value must be a string")
        return value
    
    def create(self, validated_data):
        value = validated_data['value']

        props = calculate_properties(value)

        string_obj = String.objects.create (
            value=value,
            sha256_hash=props['sha256_hash'],
            length=props['length'],
            is_palindrome=props['is_palindrome'],
            unique_characters=props['unique_characters'],
            word_count=props['word_count'],
            character_frequency_map=props['character_frequency_map'] 
        )

        return string_obj
    

class StringListSerializer(serializers.Serializer):
    data = StringSerializer(many=True)
    count = serializers.IntegerField()
    filters_applied = serializers.DictField(required=False)