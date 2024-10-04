from rest_framework import serializers
from .models import Breed, Kitten, Rating


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name']


class KittenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitten
        fields = ['id', 'breed', 'color', 'age', 'description', 'owner']
        read_only_fields = ['owner']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['kitten', 'rating']

    def validate(self, data):
        if self.context['request'].user == data['kitten'].owner:
            raise serializers.ValidationError("You cannot rate your own kitten.")
        return data
