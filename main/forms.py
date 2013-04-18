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
        instance.save()
        return instance

    class Meta:
        model = Clipping
        fields = ('title', 'tags', 'source_url')
