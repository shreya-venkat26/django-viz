from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_document, name='upload'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/<int:document_id>/', views.conversation_list, name='convo_list'),
    path('documents/delete/<int:document_id>/', views.delete_document, name='delete_document'),
    path('documents/rename/<int:document_id>/', views.rename_document, name='rename_document'),
    path('documents/analysis/<int:document_id>/', views.document_analysis, name='document_analysis')
]
