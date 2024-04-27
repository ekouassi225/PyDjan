from django.urls import path
from . import views

app_name = "monblog"

urlpatterns = [
    path('', views.index, name='index'),
    path('page_accueil/', views.accueil, name='accueil'),
    path('nos_transactions/', views.transaction, name='transaction'),
    path('mon_objectif/', views.goal, name='goal'),

]