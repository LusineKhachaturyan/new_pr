from django.forms import ModelForm, fields, widgets
from .models import Message
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['title','body']
        widgets = {
            'description': forms.Textarea(attrs={ 'class': 'form-control' }),
        }