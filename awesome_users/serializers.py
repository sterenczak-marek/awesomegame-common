from rest_framework import serializers

from .models import GameUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameUser
        fields = ['username', 'is_admin', 'ready_to_play']
