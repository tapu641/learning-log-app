from django.urls import path
from . import views

app_name = 'learning_logs'

urlpatterns = [
    # トップページ (http://127.0.0.1:8000/)
    path('', views.index, name='index'),
    path('new_log/',views.new_log, name='new_log'),
    path('edit_log/<int:log_id>',views.edit_log,name='edit_log'),
    path('delete_log/<int:log_id>/', views.delete_log, name='delete_log'),
]