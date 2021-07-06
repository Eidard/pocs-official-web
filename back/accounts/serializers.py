from rest_framework import serializers
from .models import Account
from django.contrib.auth.models import User

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class AccountSerializerInPost(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name')

class AccountSerializerInSearch(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'generation')

class AccountDetailSerializerForAnonymousUser(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('name', 'generation', 'gender')

class AccountDetailSerializerForNonAnonymousUser(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('name', 'student_id', 'generation', 'gender', 'birth', 'phone')