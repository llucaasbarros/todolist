from rest_framework import serializers


class HolidaySerializer(serializers.Serializer):
    date = serializers.DateField()
    name = serializers.CharField()
    type = serializers.CharField()
