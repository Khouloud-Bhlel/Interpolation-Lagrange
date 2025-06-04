from rest_framework import serializers
from .models import InterpolationPoint, InterpolationSet, LagrangeResult

class InterpolationPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterpolationPoint
        fields = ['id', 'x', 'y', 'created_at']

class InterpolationSetSerializer(serializers.ModelSerializer):
    points = InterpolationPointSerializer(many=True, read_only=True)
    points_count = serializers.SerializerMethodField()
    
    class Meta:
        model = InterpolationSet
        fields = ['id', 'name', 'description', 'points', 'points_count', 'created_at', 'updated_at']
    
    def get_points_count(self, obj):
        return obj.points.count()

class LagrangeResultSerializer(serializers.ModelSerializer):
    interpolation_set_name = serializers.CharField(source='interpolation_set.name', read_only=True)
    coefficients = serializers.SerializerMethodField()
    evaluation_data = serializers.SerializerMethodField()
    
    class Meta:
        model = LagrangeResult
        fields = ['id', 'interpolation_set', 'interpolation_set_name', 
                 'coefficients', 'evaluation_data', 'created_at']
    
    def get_coefficients(self, obj):
        try:
            return obj.get_coefficients()
        except:
            return []
    
    def get_evaluation_data(self, obj):
        try:
            points, results = obj.get_evaluation_data()
            return {'points': points, 'results': results}
        except:
            return {'points': [], 'results': []}

class InterpolationRequestSerializer(serializers.Serializer):
    points = serializers.ListField(
        child=serializers.ListField(
            child=serializers.FloatField(),
            min_length=2,
            max_length=2
        ),
        min_length=2
    )
    x_values = serializers.ListField(
        child=serializers.FloatField(),
        required=False,
        allow_empty=True
    )
    name = serializers.CharField(max_length=200, required=False, default="Untitled Set")
    description = serializers.CharField(required=False, allow_blank=True, default="")
