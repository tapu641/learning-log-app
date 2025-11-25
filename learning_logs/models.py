from django.db import models
from django.utils import timezone

# 1. カテゴリー（科目）のモデル
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="カテゴリー名")
    
    def __str__(self):
        return self.name

# 2. 学習ログのモデル
class LearningLog(models.Model):
    # カテゴリーとの紐付け（カテゴリーが消えたら、ログも消える設定）
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="カテゴリー")
    
    title = models.CharField(max_length=200, verbose_name="タイトル")
    study_time = models.IntegerField(verbose_name="学習時間(分)") # グラフ用の数値
    date = models.DateField(default=timezone.now, verbose_name="学習日")
    memo = models.TextField(blank=True, verbose_name="詳細メモ")
    
    # 記録した日時（自動入力）
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.study_time}分)"