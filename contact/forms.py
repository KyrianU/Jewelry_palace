from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Form for contact submission
    """
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5}),
            'subject': forms.Select(attrs={
                'class': 'form-control select form-select',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
