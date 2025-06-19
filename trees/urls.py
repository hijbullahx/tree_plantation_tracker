from django.urls import path
from . import views
from . import views_additional

urlpatterns = [
    path('', views.tree_list, name='tree_list'),
    path('<int:pk>/', views.tree_detail, name='tree_detail'),
    path('add/', views.add_tree, name='add_tree'),
    path('task/<int:task_id>/complete/', views.mark_task_completed, name='mark_task_completed'),
    path('<int:pk>/add_health_log/', views_additional.add_health_log, name='add_health_log'),
    path('<int:pk>/add_task/', views_additional.add_task, name='add_task'),
]
