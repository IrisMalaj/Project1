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

    def __str__(self):
        return self.name

class Review(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    user_name = models.CharField(max_length=100)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.guide.name if self.guide else 'General'} by {self.user_name}"

