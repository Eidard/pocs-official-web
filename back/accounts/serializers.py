from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class AccountSerializerInPost(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name')