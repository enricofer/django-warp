from django import forms
from django.forms import ModelForm
from .models import datasets


class UploadImmagineSorgenteForm(forms.Form):
    titolo = forms.CharField(max_length=50)
    note = forms.CharField(max_length=250)
    sorgente = forms.FileField()
    titolo.widget.attrs['class'] = 'form-control'
    note.widget.attrs['class'] = 'form-control'
    #sorgente.widget.attrs['class'] = 'form-control'

class BaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name[:6] == 'extent':
                field.widget.attrs['class'] = 'hidden'
            else:
                if field_name[:6] != 'transp':
                    field.widget.attrs['class'] = 'form-control'

class DatasetForm(BaseForm):
    class Meta:
        model = datasets
        exclude = ['slug',]

    def clean_name(self):
        name = self.cleaned_data['name']
        if name == "__TRASH":
            raise forms.ValidationError("'__TRASH' is a reserved dataset name")
        return name
