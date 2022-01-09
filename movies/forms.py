from django import forms
from .models import Vote, Review


class MovieRatingForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = ('value',)


class MovieReviewForm(forms.ModelForm):
    body_text = forms.Textarea()

    class Meta:
        model = Review
        fields = ('text',)
