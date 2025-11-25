from django.contrib import admin
# 作ったモデルを読み込む
from .models import Category, LearningLog

# 管理画面に登録する
admin.site.register(Category)
admin.site.register(LearningLog)