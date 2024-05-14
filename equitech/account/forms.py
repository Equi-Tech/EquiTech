from django import forms
from .models import KYC
from django.forms import ImageField, FileInput, DateInput


class DateInput(forms.DateInput):
    input_type = 'date'


class KYCForm(forms.ModelForm):
    identify_image = ImageField(widget=FileInput)
    image = ImageField(widget=FileInput)
    signature = ImageField(widget=FileInput)

    class Meta:
        model = KYC
        fields = [
            'full_name',
            'image',
            'marital_status',
            'gender',
            'identity_type',
            'identity_image',
            'date_of_birth',
            'signature',
            'country',
            'state',
            'city',
            'mobile',
            'fax',
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder" : "Full Name"}),
            # "image": forms.TextInput(attrs={"placeholder" : "Full Name"}),
            # "marital_status": forms.TextInput(attrs={"placeholder" : "Full Name"}),
            # "gender": forms.TextInput(attrs={"placeholder" : "Full Name"}),
            # "identity_type": forms.TextInput(attrs={"placeholder" : "Full Name"}),
            # "identity_image": forms.TextInput(attrs={"placeholder" : "Full Name"}),
            "date_of_birth": DateInput,
            # "signature": forms.TextInput(attrs={"placeholder" : "Full Name"}),
            "country": forms.TextInput(attrs={"placeholder" : "Country"}),
            "state": forms.TextInput(attrs={"placeholder" : "State"}),
            "city": forms.TextInput(attrs={"placeholder" : "City"}),
            "mobile": forms.TextInput(attrs={"placeholder" : "Mobile Number"}),
            "fax": forms.TextInput(attrs={"placeholder" : "Fax"}),
        }