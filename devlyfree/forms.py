from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre Nom*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre Email*'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Votre Site Web'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre Commentaire*'}),
        }
