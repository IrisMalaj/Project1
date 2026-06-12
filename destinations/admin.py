from django.contrib import admin
from .models import Destination, Guide, Review, Itinerary, ItineraryDay

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    search_fields = ('name', 'category')

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'rating', 'category', 'languages')
    list_filter = ('category',)
    search_fields = ('name', 'specialty')
    fields = ('name', 'specialty', 'bio', 'avatar_url', 'rating', 'review_count', 'category', 'languages')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer_name_display', 'guide', 'rating', 'reviewer_country', 'is_visible', 'created_at')
    list_filter = ('rating', 'is_visible', 'created_at', 'guide')
    search_fields = ('reviewer_name', 'user_name', 'review_text', 'comment')
    fields = ('guide', 'reviewer_name', 'user_name', 'reviewer_country', 'rating', 'review_text', 'comment', 'is_visible')

    def reviewer_name_display(self, obj):
        return obj.reviewer_name or obj.user_name or "Anonymous"
    reviewer_name_display.short_description = 'Reviewer Name'

class ItineraryDayInline(admin.TabularInline):
    model = ItineraryDay
    extra = 1
    ordering = ['day_number']

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    inlines = [ItineraryDayInline]

