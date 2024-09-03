from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit, Div
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'image_url', 'status', 'current_bid', 'category']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder':'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder':'Description with less than 500 words'}),
            'image_url': forms.TextInput(attrs={'class': 'form-control','placeholder':'Image Link or URL'}),
            'current_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title'),
            Field('description'),
            Field('image_url'),
            Div(
                Field('status', css_class='form-check-input'),
                css_class='form-check'
            ),
            Field('current_bid'),
            Field('category'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            )
        )
