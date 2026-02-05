# client_project/api/serializers.py
from rest_framework import serializers
from waffle.models import Flag

class WaffleFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = ['name', 'everyone', 'note']