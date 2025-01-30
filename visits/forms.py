from django import forms

class ExcelUploadForm(forms.Form):
    file = forms.FileField(label='Excel Faylı Yükləyin', widget=forms.FileInput(attrs={
        'accept': '.xls,.xlsx'
    }))
