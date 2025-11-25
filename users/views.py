from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm # ★Django標準の登録フォーム

def register(request):
    """新しいユーザーを登録する"""
    if request.method != 'POST':
        # フォームを表示する（空のフォーム）
        form = UserCreationForm()
    else:
        # フォームを処理する
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # 登録と同時にログインさせる
            login(request, new_user)
            return redirect('learning_logs:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)