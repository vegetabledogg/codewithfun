"""
from django import forms
from judge.models import Lesson, Submission

class SubmissionForm(forms.ModelForm):
    code = forms.CharField(widget=forms.Textarea)
        
    class Meta:
        model = Submission
<<<<<<< HEAD
        fields = ['code']
=======
        field = ['code']
"""
>>>>>>> 6633dbff8eabd068182a1ff199280065dfae3bdd
