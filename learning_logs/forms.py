from django import forms
from .models import Category, LearningLog # Categoryを追加

# ★1. 新しいカテゴリーを作るためのフォーム
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': '新しいカテゴリー名'}

# ★2. ログを記録するフォーム（修正版）
class LearningLogForm(forms.ModelForm):
    class Meta:
        model = LearningLog
        fields = ['category', 'title', 'study_time', 'date', 'memo']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'study_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'memo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    # ★重要テクニック: フォームを作る瞬間に「ユーザー情報」を受け取る
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # カテゴリーの選択肢を「そのユーザーのもの」だけに絞り込む
        self.fields['category'].queryset = Category.objects.filter(owner=user)