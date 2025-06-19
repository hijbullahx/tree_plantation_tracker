from django.urls import path
from . import views

urlpatterns = [
    path('', views.tree_list, name='tree_list'),
    path('<int:pk>/', views.tree_detail, name='tree_detail'),
    path('add/', views.add_tree, name='add_tree'),  # ← new line
]
