# Generated manually for Reviews system extension in nested project

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0003_itinerary_remove_tourday_tour_itineraryday_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='languages',
            field=models.CharField(blank=True, default='English, Albanian', max_length=200),
        ),
        migrations.AddField(
            model_name='review',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='review',
            name='reviewer_country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='reviewer_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='review_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
