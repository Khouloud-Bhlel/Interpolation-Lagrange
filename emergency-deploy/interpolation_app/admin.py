from django.contrib import admin
from .models import InterpolationPoint, InterpolationSet, LagrangeResult


class InterpolationPointInline(admin.TabularInline):
    model = InterpolationSet.points.through
    extra = 1


@admin.register(InterpolationPoint)
class InterpolationPointAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'x', 'y', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('x', 'y')
    ordering = ('x',)


@admin.register(InterpolationSet)
class InterpolationSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_points_count', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    inlines = [InterpolationPointInline]
    readonly_fields = ('created_at', 'updated_at')
    
    def get_points_count(self, obj):
        return obj.points.count()
    get_points_count.short_description = 'Points Count'


@admin.register(LagrangeResult)
class LagrangeResultAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'interpolation_set', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('interpolation_set__name',)
    readonly_fields = ('created_at', 'polynomial_coefficients', 'evaluation_points', 'evaluation_results')
    
    fieldsets = (
        (None, {
            'fields': ('interpolation_set', 'created_at')
        }),
        ('Mathematical Data', {
            'fields': ('polynomial_coefficients', 'evaluation_points', 'evaluation_results'),
            'classes': ('collapse',)
        }),
    )
