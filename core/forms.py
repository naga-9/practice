from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "up-validate": ""}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Contact.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email has already sent us a message.")
        return email
