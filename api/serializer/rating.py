from rest_framework import serializers

from community.models import Rating


class RatingSerializer(serializers.Serializer):

    class Meta:
        model = Rating
        fields = '__all__'
