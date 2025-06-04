from django.db import models
import json

class InterpolationPoint(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['x']
    
    def __str__(self):
        return f"Point({self.x}, {self.y})"

class InterpolationSet(models.Model):
    name = models.CharField(max_length=200, default="Untitled Set")
    description = models.TextField(blank=True)
    points = models.ManyToManyField(InterpolationPoint, related_name='sets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_points_list(self):
        return [(point.x, point.y) for point in self.points.all().order_by('x')]

class LagrangeResult(models.Model):
    interpolation_set = models.ForeignKey(InterpolationSet, on_delete=models.CASCADE)
    polynomial_coefficients = models.TextField()  # JSON string
    evaluation_points = models.TextField()  # JSON string
    evaluation_results = models.TextField()  # JSON string
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_coefficients(self, coefficients):
        self.polynomial_coefficients = json.dumps(coefficients)
    
    def get_coefficients(self):
        return json.loads(self.polynomial_coefficients)
    
    def set_evaluation_data(self, points, results):
        self.evaluation_points = json.dumps(points)
        self.evaluation_results = json.dumps(results)
    
    def get_evaluation_data(self):
        points = json.loads(self.evaluation_points)
        results = json.loads(self.evaluation_results)
        return points, results
