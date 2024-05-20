# forms.py
from django import forms

class FingerprintLoginForm(forms.Form):
    fingerprint_data = forms.CharField(label='Fingerprint Data', max_length=100)
