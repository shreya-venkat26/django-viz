from django import forms

class DocumentUploadForm(forms.Form):
    document = forms.FileField()
    document_name = forms.CharField(
        max_length=255, 
        label='Document Name', 
        widget=forms.TextInput(attrs={'placeholder': 'Enter document name:'})
    )
