from django import forms
from main.models import *


class ClippingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super (ClippingForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ClippingForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        return instance.save()


    class Meta:
        model = Clipping
        fields = ('title', 'tags', 'source_url')

class ShareForm(forms.Form):
    title = forms.CharField(required=True)
    recipients = forms.CharField(required=True, help_text="Comma-separated list of recipients")
    message = forms.CharField(widget=forms.Textarea, initial="Brought to you by SmartClip")
