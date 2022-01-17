from rest_framework import serializers

from apps.queries.models import Category, Param


class CategorySerializer(serializers.ModelSerializer):
    class QuerySerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255)
        description = serializers.CharField(max_length=1000)
        slug = serializers.CharField(max_length=255)

    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1000)
    slug = serializers.CharField(max_length=255)
    queries = QuerySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class ParamSerializer(serializers.ModelSerializer):
    class QuerySerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255)
        description = serializers.CharField(max_length=1000)
        slug = serializers.CharField(max_length=255)

    name = serializers.CharField(max_length=255)
    default = serializers.CharField(max_length=1000)
    type = serializers.CharField(max_length=255)
    query = QuerySerializer(many=False, read_only=True)

    class Meta:
        model = Param
        fields = '__all__'
