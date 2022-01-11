from django import forms
from .models import Vote, Review


class MovieRatingForm(forms.ModelForm):
    value = forms.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = Vote
        fields = ('value',)


class MovieReviewForm(forms.ModelForm):
    body_text = forms.Textarea()

    class Meta:
        model = Review
        fields = ('text',)
