from django import forms

class FeedbackForm(forms.Form):
    correct = forms.IntegerField
    id = forms.IntegerField