from django.db import models

# Models creation
class String(models.Model): #corrected strings -> Strings
    value = models.TextField(unique=True)
    length = models.IntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.IntegerField()
    word_count = models.IntegerField()
    sha256_hash = models.CharField(max_length=64, unique=True, primary_key=True)
    character_frequency_map = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'strings'

    def __str__(self):
        return self.value
