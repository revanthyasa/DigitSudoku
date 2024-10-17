# sudoku/serializers.py
from rest_framework import serializers

class SudokuSerializer(serializers.Serializer):
    grid = serializers.ListField(
        child=serializers.ListField(child=serializers.IntegerField())
    )
