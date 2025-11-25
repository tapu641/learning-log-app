from django import forms
from .models import LearningLog

class LearningLogForm(forms.ModelForm):
    class Meta:
        model = LearningLog
        # フォームに入力させたい項目を選びます
        fields = ['category', 'title', 'study_time', 'date', 'memo']
        # カレンダー入力ができるようにする設定（これがないと文字入力になって不便です）
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'study_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'memo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }