from django import forms
from .models import Review

class NewReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'rating', 'description')
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
        }

class EditReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'rating', 'description')
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
        }
