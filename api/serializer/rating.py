from rest_framework import serializers

from community.models import Rating


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['rating_star','user']
        read_only_fields = ['user']