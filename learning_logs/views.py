from django.shortcuts import render, redirect
from django.db.models import Sum
from django.utils import timezone
import datetime
from .models import Category, LearningLog
from .forms import LearningLogForm

def index(request):
    """学習ログのトップページを表示する"""
    # 1. 既存のリスト表示用データ
    logs = LearningLog.objects.order_by('-date')

    # --- グラフ用のデータ作成 ---
    
    # 今日の日付を取得
    today = timezone.now().date()

    # 【円グラフ用】今日の学習内訳（カテゴリーごと）
    categories = Category.objects.all()
    pie_labels = [] # ラベル（Python, 英語など）
    pie_data = []   # データ（30分, 60分など）

    for cat in categories:
        # そのカテゴリーで、かつ「今日」の合計時間を計算
        total = LearningLog.objects.filter(category=cat, date=today).aggregate(Sum('study_time'))['study_time__sum']
        if total: # データがある場合のみリストに追加
            pie_labels.append(cat.name)
            pie_data.append(total)

    # 【棒グラフ用】過去7日間の日別学習時間
    bar_labels = [] # 日付（11/24, 11/25など）
    bar_data = []   # 合計時間

    for i in range(6, -1, -1): # 6日前から今日(0)までループ
        date = today - datetime.timedelta(days=i)
        # その日の合計時間を計算
        total = LearningLog.objects.filter(date=date).aggregate(Sum('study_time'))['study_time__sum']
        
        bar_labels.append(date.strftime('%m/%d')) # 日付を文字列にする
        bar_data.append(total if total else 0)    # データがないなら0を入れる

    # テンプレートに渡すデータ
    context = {
        'logs': logs,
        'pie_labels': pie_labels,
        'pie_data': pie_data,
        'bar_labels': bar_labels,
        'bar_data': bar_data,
    }
    
    return render(request, 'learning_logs/index.html', context)

def new_log(request):
    """新しい学習ログを登録する"""
    if request.method != 'POST':
        # データが送信されていない時は、空のフォームを作る
        form = LearningLogForm()
    else:
        # POSTでデータが届いた時は、中身を処理する
        form = LearningLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:index') # 保存したらトップページに戻る

    # ページを表示する
    context = {'form': form}
    return render(request, 'learning_logs/new_log.html', context)

def edit_log(request, log_id):
    """既存のログを編集する"""
    # 編集したいデータをIDを使ってデータベースから探してくる
    log = LearningLog.objects.get(id=log_id)

    if request.method != 'POST':
        # 初回表示：保存されているデータ(instance=log)が入ったフォームを作る
        form = LearningLogForm(instance=log)
    else:
        # 送信時：送られてきたデータで上書き保存する
        form = LearningLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:index')

    context = {'log': log, 'form': form}
    return render(request, 'learning_logs/edit_log.html', context)

def delete_log(request, log_id):
    """ログを削除する"""
    # 削除したいデータを取得
    log = LearningLog.objects.get(id=log_id)
    
    if request.method == 'POST':
        # 「削除実行」ボタンが押されたら、実際に消す
        log.delete()
        return redirect('learning_logs:index')
    
    # 削除確認ページを表示
    context = {'log': log}
    return render(request, 'learning_logs/delete_log.html', context)