from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.CharField(max_length=500, help_text="Path to image (e.g., tours/images/tirane.jpg)")
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Guide(models.Model):
    name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=200)
    bio = models.TextField()
    avatar_url = models.CharField(max_length=500, blank=True, null=True)
    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)
    category = models.CharField(max_length=100) # e.g., 'hiking', 'history'
    languages = models.CharField(max_length=200, blank=True, default='English, Albanian')

    def __str__(self):
        return self.name

class Review(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    user_name = models.CharField(max_length=100) # Keep for destination/general comments
    reviewer_name = models.CharField(max_length=100, blank=True, null=True)
    reviewer_country = models.CharField(max_length=100, blank=True, null=True)
    rating = models.IntegerField(default=5)
    comment = models.TextField() # Keep for destination/general comments
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)

    @property
    def reviewer_name_display(self):
        return self.reviewer_name or self.user_name or "Anonymous"

    @property
    def review_text_display(self):
        return self.review_text or self.comment

    def __str__(self):
        reviewer = self.reviewer_name_display
        guide_name = self.guide.name if self.guide else 'General'
        return f"Review for {guide_name} by {reviewer} ({self.rating} stars)"
