from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, LearningLog
from .forms import LearningLogForm, CategoryForm
from django.db.models import Sum
from django.utils import timezone
import datetime
# ★ログイン必須にするための魔法
from django.contrib.auth.decorators import login_required
from django.http import Http404

def index(request):
    """学習ログのトップページを表示する"""
    # ★ログインしていない場合、公開ページとして見せるか、ログイン画面に飛ばすか。
    # ここでは「ログイン画面に飛ばす」設定にします。
    if not request.user.is_authenticated:
        return redirect('users:login')

    # ★自分のデータだけを取得するフィルター (owner=request.user)
    logs = LearningLog.objects.filter(owner=request.user).order_by('-date')

    # --- グラフ用のデータ作成 (ここも自分のデータだけに限定) ---
    today = timezone.now().date()
    
    # 円グラフ（自分のデータで集計）
    categories = Category.objects.filter()
    pie_labels = []
    pie_data = []
    for cat in categories:
        # filterに owner=request.user を追加
        total = LearningLog.objects.filter(category=cat, date=today, owner=request.user).aggregate(Sum('study_time'))['study_time__sum']
        if total:
            pie_labels.append(cat.name)
            pie_data.append(total)

    # 棒グラフ（自分のデータで集計）
    bar_labels = []
    bar_data = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        # filterに owner=request.user を追加
        total = LearningLog.objects.filter(date=date, owner=request.user).aggregate(Sum('study_time'))['study_time__sum']
        bar_labels.append(date.strftime('%m/%d'))
        bar_data.append(total if total else 0)

    context = {
        'logs': logs,
        'pie_labels': pie_labels,
        'pie_data': pie_data,
        'bar_labels': bar_labels,
        'bar_data': bar_data,
    }
    return render(request, 'learning_logs/index.html', context)

@login_required # ★ログイン必須
def new_log(request):
    """新しい学習ログを登録する"""
    if request.method != 'POST':
        form = LearningLogForm(user=request.user)
    else:
        form = LearningLogForm(request.user, data=request.POST)
        if form.is_valid():
            # ★重要: すぐに保存せず(commit=False)、持ち主情報をセットしてから保存する
            new_log = form.save(commit=False)
            new_log.owner = request.user
            new_log.save()
            return redirect('learning_logs:index')

    context = {'form': form}
    return render(request, 'learning_logs/new_log.html', context)

@login_required
def edit_log(request, log_id):
    """既存のログを編集する"""
    log = get_object_or_404(LearningLog, id=log_id)
    
    # ★他人のデータならエラーにする（URL直接入力対策）
    if log.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = LearningLogForm(user=request.user, instance=log)
    else:
        form = LearningLogForm(request.user, instance=log, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:index')

    context = {'log': log, 'form': form}
    return render(request, 'learning_logs/edit_log.html', context)

@login_required
def delete_log(request, log_id):
    """ログを削除する"""
    log = get_object_or_404(LearningLog, id=log_id)
    
    # ★他人のデータならエラーにする
    if log.owner != request.user:
        raise Http404
    
    if request.method == 'POST':
        log.delete()
        return redirect('learning_logs:index')
    
    context = {'log': log}
    return render(request, 'learning_logs/delete_log.html', context)

@login_required
def new_category(request):
    """新しいカテゴリーを追加する"""
    if request.method != 'POST':
        form = CategoryForm()
    else:
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            new_cat = form.save(commit=False)
            new_cat.owner = request.user # 持ち主をセット
            new_cat.save()
            # 保存したら、ログの投稿画面に飛ばしてあげると親切
            return redirect('learning_logs:new_log')
            
    context = {'form': form}
    return render(request, 'learning_logs/new_category.html', context)