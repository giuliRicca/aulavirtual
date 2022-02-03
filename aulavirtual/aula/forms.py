from django import forms
from .models import Response, Assignment


class ResponseForm(forms.ModelForm):
    text_response = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 4
    }))

    class Meta:
        model = Response
        fields = ('text_response', 'response_file')


class AssignmentForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Titulo'
    }))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Descripcion (opcional)',
    }))

    due_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={
        'class': 'form-control',
        'type': 'datetime-local',
        'data-date-format': "dd-mm",
    }))

    class Meta:
        model = Assignment
        fields = ('title', 'description', 'assigment_file', 'due_date')
