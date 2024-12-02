from django import forms

from games.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["comment", "rating"]

    widgets = {
        "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Your Review"}),
        "rating": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
    }
