from django import forms

class BarcodeForm(forms.Form):
    excel_file = forms.FileField()
    folder_name = forms.CharField(max_length=100)
