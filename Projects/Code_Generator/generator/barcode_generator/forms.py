from django import forms

class BarcodeForm(forms.Form):
    excel_file = forms.FileField()
    folder_name = forms.CharField(max_length=100)

class QRCodeForm(forms.Form):
    excel_file = forms.FileField(widget=forms.FileInput())
    folder_name = forms.CharField(max_length=100, required=False)