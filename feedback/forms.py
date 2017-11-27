from django import forms

class FeedbackForm(forms.Form):
    correct = forms.CharField()
    id = forms.CharField()