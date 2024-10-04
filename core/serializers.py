from rest_framework import serializers
from .models import Cat, Kind, Rating


class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kind
        fields = ['id', 'name']


class CatSerializer(serializers.ModelSerializer):
    kind_id = serializers.PrimaryKeyRelatedField(
        queryset=Kind.objects.all(),
        source='kind',
        write_only=True,
    )

    class Meta:
        model = Cat
        fields = ['id', 'color', 'age', 'description', 'user', 'kind', 'kind_id', 'average_rating']
        read_only_fields = ['user', 'kind']

    def create(self, validated_data):
        return super().create(validated_data)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['score']

    def validate_score(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Оценка должна быть в диапазоне от 1 до 5.")
        return value
