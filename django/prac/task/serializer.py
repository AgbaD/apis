from rest_framework import serializers
from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['firstname', 'lastname', 'email', 'number', 'public_id']


class PlayerRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

