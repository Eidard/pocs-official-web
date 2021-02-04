from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.Serializer):
    class Meta:
        model = Account
        field = ['username', 'password', 'name', 'email', 'generation', 'student_id', 'gender', 'birth', 'phone', 'joined_at', 'is_approved']

        
