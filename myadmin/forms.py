from django import forms
from judge.models import Lesson

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        exclude = []