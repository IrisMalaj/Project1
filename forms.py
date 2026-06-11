from django import forms
from .models import Review, Guide

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['guide', 'reviewer_name', 'reviewer_country', 'rating', 'review_text']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['guide'].queryset = Guide.objects.all()
        self.fields['guide'].empty_label = "Select a Guide / Staff member"
        self.fields['guide'].widget.attrs.update({'class': 'form-select rounded-3 p-3 shadow-sm border'})
        self.fields['reviewer_name'].widget.attrs.update({'class': 'form-control rounded-3 p-3 shadow-sm border', 'placeholder': 'Your Full Name'})
        self.fields['reviewer_country'].widget.attrs.update({'class': 'form-control rounded-3 p-3 shadow-sm border', 'placeholder': 'Your Country (Optional)'})
        self.fields['rating'].widget.attrs.update({'class': 'form-select rounded-3 p-3 shadow-sm border'})
        self.fields['rating'].choices = [(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]
        self.fields['review_text'].widget.attrs.update({'class': 'form-control rounded-3 p-3 shadow-sm border', 'rows': 5, 'placeholder': 'Describe your experience with the guide...'})

        # Ensure reviewer_name and review_text are explicitly required
        self.fields['reviewer_name'].required = True
        self.fields['review_text'].required = True

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5 stars.")
        return rating
