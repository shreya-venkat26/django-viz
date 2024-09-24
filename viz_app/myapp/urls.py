from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_document, name='upload'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/<int:document_id>/', views.conversation_list, name='convo_list'),
]
