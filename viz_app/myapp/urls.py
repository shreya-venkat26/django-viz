from django.urls import path
from . import views

urlpatterns = [
    ##path("", views.home, "home"),
    path('upload/', views.upload_document, name='upload_document'),
    path('conversations/', views.conversation_list, name='convo_list')
]