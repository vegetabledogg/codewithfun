from django import forms
from judge.models import Lesson, Submission

class SubmissionForm(forms.ModelForm):
    code = forms.CharField(widget=forms.Textarea)
        
    class Meta:
        model = Submission
        fields = ['code']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        exclude = []
