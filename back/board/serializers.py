from rest_framework import serializers
from .models import Board, Board_Category

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name', 'description')

class BoardCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Board_Category
        fields = ('id', 'name')